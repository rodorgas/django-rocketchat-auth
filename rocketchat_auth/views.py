import requests

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from .decorators import cors_allow_credentials
from pymongo import MongoClient
from rocketchat_auth import helpers


def home(request):
    return render(request, 'home.html')


def redirect_rocketchat(request):
    return redirect(settings.ROCKETCHAT_URL)


@cors_allow_credentials()
@xframe_options_exempt
def api(request):
    """
    Implements API for Rocket.Chat IFrame authentication
    """
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    client = MongoClient("mongodb://" + settings.MONGO_DB)
    mongo = client.rocketchat

    user = mongo.users.find_one({'username': request.user.username})
    if not user:
        fullname = ' '.join([request.user.first_name, request.user.last_name])\
                      .strip()

        headers = {
            'X-Auth-Token': ROCKETCHAT_AUTH_TOKEN,
            'X-User-Id': ROCKETCHAT_USER_ID,
        }
        data = {
            'email': request.user.email,
            'name': request.user.name,
            'username': request.user.username,
            'password': helpers.generate_token(),
        }
        requests.get(settings.ROCKETCHAT_URL + '/api/v1/users.create',
                    headers=headers, data=data)

        user = mongo.users.find_one({'username': request.user.username})

    user['services'] = {'iframe': {'token': helpers.generate_token()}}
    mongo.users.update_one({'_id': user['_id']}, {'$set': user})


    return JsonResponse({
        'token': user['services']['iframe']['token'],
    })
