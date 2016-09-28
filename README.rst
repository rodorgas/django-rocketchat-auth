django-rocketchat-auth
======================

.. image:: https://img.shields.io/pypi/v/django-rocketchat-auth.svg
    :target: https://pypi.python.org/pypi/django-rocketchat-auth

Authenticate your `Rocket.Chat`_ users with Django web framework.

This app implements the API used by `Rocket.Chat IFrame authentication`_. Also, it handles logout by wiring up a method on Django signals.


Quickstart
----------

1. Install this app in you project::

    pip install django-rocketchat-auth

2. Add "rocketchat_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'rocketchat_auth',
    )

3. Update your `settings.py`::

    MONGO_DB = 'localhost:27017'
    ROCKETCHAT = 'localhost'

4. Include the rocketchat_auth URLconf in your project urls.py like this::

    urlpatterns += [url(r'^rocketchat/', include('rocketchat_auth.urls'))]

5. You will probably need to use `django-cors-headers`_ and set your Rocket.Chat domain in `CORS_ORIGIN_WHITELIST`

6. Now go to your Rocket.Chat admin page > Settings > Accounts. Enable **Iframe** and set:

 - **Iframe URL**: http://localhost:8000/login/?next=/rocketchat/redirect (assuming you have a login page in /login)
 - **URL API**: http://localhost:8000/rocketchat/api


Roadmap
-------

- Enforce unique email registration in Django admin, since Rocket.Chat requires this.
- Update Rocket.Chat user details in MongoDB when the user is modified in Django Admin.

.. _`Rocket.Chat`: https://github.com/RocketChat/Rocket.Chat) users using [Django framework](https://github.com/django/django
.. _`Rocket.Chat IFrame authentication`: https://rocket.chat/docs/administrator-guides/authentication/iframe/
.. _`django-cors-headers`: https://github.com/ottoyiu/django-cors-headers
