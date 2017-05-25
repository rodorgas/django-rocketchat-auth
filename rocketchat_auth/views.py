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

    fullname = ' '.join([request.user.first_name, request.user.last_name])\
                  .strip()

    return helpers.create_user(request.email, fullname, request.username)
