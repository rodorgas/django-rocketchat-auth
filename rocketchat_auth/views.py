from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse

from pymongo import MongoClient

import datetime
import hashlib
import string
import random

from .decorators import cors_allow_credentials


def home(request):
    return render(request, 'home.html')


def redirect_rocketchat(request):
    return redirect(settings.ROCKETCHAT)


def generate_id():
    n = 17
    chars = string.ascii_letters + string.digits
    random_id = ''.join(random.SystemRandom().choice(chars) for _ in range(n))

    return random_id


@cors_allow_credentials()
def api(request):
    """
    Implements API for Rocket.Chat IFrame authentication
    """
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    # Try to get user in mongo
    client = MongoClient("mongodb://" + settings.MONGO_DB)
    mongo = client.rocketchat

    user = mongo.users.find_one({'username': request.user.username})
    user_created = False

    if not user:
        # Create the user if doesn't exist in mongo
        user_created = True
        fullname = ' '.join([request.user.first_name, request.user.last_name])\
                      .strip()

        user = {
            '_id': generate_id(),
            'createdAt': datetime.datetime.now(),
            'emails': [{
                'address': request.user.email,
                'verified': True
            }],
            'name': fullname,
            'username': request.user.username,
            'active': True,
            'roles': [
                'user'
            ],
            'type': 'user',
            'avatarOrigin': 'gravatar',

            'status': 'away',
            'statusConnection': 'online',
            'utcOffset': -3,
            'statusDefault': 'away'
        }

        mongo.users.insert_one(user)

    # Generate token
    n = 50
    chars = string.ascii_letters + string.digits
    token = ''.join(random.SystemRandom().choice(chars) for _ in range(n))
    token = hashlib.sha1(token.encode()).hexdigest()

    user['services'] = {'iframe': {'token': token}}

    # Save the user back to mongo
    mongo.users.update_one({'_id': user['_id']}, {'$set': user})

    if user_created:
        # Add the user to default channels
        mongo.rocketchat_room.update(
            {'default': True},
            {'$addToSet': {'usernames': request.user.username}},
        )

        default_rooms = mongo.rocketchat_room.find({'default': True})
        for default_room in default_rooms:

            subscription = mongo.users.find_one({
                'rid': default_room['_id'],
                'u': {'_id': user['_id']},
            })

            if not subscription:
                now = datetime.datetime.now()

                subscription = {
                    '_id': generate_id(),
                    'open': True,
                    'alert': False,
                    'unread': 0,
                    'ts': now,
                    'rid': default_room['_id'],
                    'name': default_room['name'],
                    't': 'c',
                    'u': {'_id': user['_id'], 'username': user['username']},
                    '_updatedAt': now,
                    'ls': now,
                }

                mongo.rocketchat_subscription.insert_one(subscription)

    return JsonResponse({
        'token': user['services']['iframe']['token'],
    })
