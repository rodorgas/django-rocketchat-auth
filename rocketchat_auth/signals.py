from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

from pymongo import MongoClient
from django.conf import settings


@receiver(user_logged_out)
def logout(sender, user, request, **kwargs):
    client = MongoClient("mongodb://" + settings.MONGO_DB)
    mongo = client.rocketchat

    mongo.users.update(
        {'username': request.user.username},
        {
            '$set': {'services': {'iframe': {'token': ''}}}
        }
    )
