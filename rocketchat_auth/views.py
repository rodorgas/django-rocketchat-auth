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


@cors_allow_credentials()
def api(request):
    """
    Implements API for Rocket.Chat IFrame authentication

    https://rocket.chat/docs/administrator-guides/authentication/iframe/
    """
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    # Try to get user in mongo
    client = MongoClient("mongodb://" + settings.MONGO_DB)
    mongo = client.rocketchat

    user = mongo.users.find_one({'username': request.user.username})

    if not user:
        # Create the user if doesn't exist in mongo
        n = 17
        chars = string.ascii_letters + string.digits
        user_id = ''.join(random.SystemRandom().choice(chars) for _ in range(n))

        user = {
            '_id': user_id,
            'createdAt': datetime.datetime.now(),
            'emails': [{
                'address': request.user.email,
                'verified': True
            }],
            'name': ' '.join([request.user.first_name, request.user.last_name]).strip(),
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


    # Add the user to default channels
    mongo.rocketchat_room.update(
        {'default': True},
        {'$addToSet': {'usernames': request.user.username}},
    )

    return JsonResponse({
        'token': user['services']['iframe']['token'],
    })
