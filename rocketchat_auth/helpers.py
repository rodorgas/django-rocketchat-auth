import hashlib
import random
import string
import requests
from pymongo import MongoClient
from django.conf import settings


def generate_token(n=50):
    chars = string.ascii_letters + string.digits
    token = ''.join(random.SystemRandom().choice(chars) for _ in range(n))
    token = hashlib.sha1(token.encode()).hexdigest()

    return token


def create_user(email, fullname, username):
    client = MongoClient("mongodb://" + settings.MONGO_DB)
    if '/' in settings.MONGO_DB:
        mongo = client.get_default_database()
    else:
        mongo = client.rocketchat

    user = mongo.users.find_one({'username': username})
    if not user:

        headers = {
            'X-Auth-Token': settings.ROCKETCHAT_AUTH_TOKEN,
            'X-User-Id': settings.ROCKETCHAT_USER_ID,
        }
        data = {
            'email': email,
            'name': fullname,
            'username': username,
            'password': generate_token(),
        }
        resp = requests.post(settings.ROCKETCHAT_URL + '/api/v1/users.create',
                             headers=headers, data=data, verify=False)
        if resp.status_code != 200:
            raise Exception('Could not create user')

        user = mongo.users.find_one({'username': username})

    user['services'] = {'iframe': {'token': generate_token()}}
    mongo.users.update_one({'_id': user['_id']}, {'$set': user})

    return user['services']['iframe']['token']
