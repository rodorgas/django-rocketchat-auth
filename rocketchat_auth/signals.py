from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings
from pymongo import MongoClient
import requests
import logging


logger = loggin.getLogger('dm.log')

@receiver(user_logged_out)
def logout(sender, user, request, **kwargs):
    logger.error('teste')
    client = MongoClient("mongodb://" + settings.MONGO_DB)
    mongo = client.rocketchat

    mongo.users.update(
        {'username': request.user.username},
        {
            '$set': {'services': {'iframe': {'token': ''}}}
        }
    )


@receiver(post_save, sender=User)
def update_user(sender, **kwargs):
    logger.error('usr updated')
    print(update_fields)
