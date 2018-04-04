django-rocketchat-auth
======================

.. image:: https://img.shields.io/pypi/v/django-rocketchat-auth.svg
    :target: https://pypi.python.org/pypi/django-rocketchat-auth

Authenticate your `Rocket.Chat`_ users with Django web framework.

This app implements the API used by `Rocket.Chat IFrame authentication`_. Also, it handles logout by wiring up a method on Django signals.

It was tested with Django 2.0.4 and Rocket.Chat 0.62.2. If you have any problems, please open an issue.

Quickstart
----------

1. Install this app in you project::

    pip install django-rocketchat-auth

2. Add "rocketchat_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'rocketchat_auth',
    )

3. `Get an Rocket.Chat authentication token`_, so we can use the API.

4. Update your `settings.py`::

    MONGO_DB = 'localhost:27017'

    ROCKETCHAT_URL = 'http://localhost:3000'
    # or more verbose (e.g. for Heroku)
    # ROCKETCHAT = '<dbuser>:<dbpassword>@<dbhost>:<dbport>/<dbname>?authSource=<dbname>'

    ROCKETCHAT_AUTH_TOKEN = '<YOUR AUTH TOKEN>'
    ROCKETCHAT_USER_ID = '<YOUR USER ID>'

    CORS_ORIGIN_WHITELIST = (
        'localhost:8000',
        'localhost:3000',
    )


5. Include the rocketchat_auth URLconf in your project urls.py like this::

    urlpatterns += [url(r'^rocketchat/', include('rocketchat_auth.urls'))]

6. Since we will put your Django app into an iframe, we have to setup some security measures that would prevent it from happening:

 - Install `django-cors-headers`_ and set your Rocket.Chat domain in `CORS_ORIGIN_WHITELIST`
 - Configure Django's `XFrameOptionsMiddleware` to exempt your login page for Rocket.Chat requests or disable it (dangerous)
 - Configure Django's `CsrfViewMiddleware` to exempt your login page for Rocket.Chat requests or disable it (dangerous)

7. Now go to your Rocket.Chat admin page > Accounts > Iframe:

 - Enable **Iframe**
 - **Iframe URL**: http://localhost:8000/admin/login/?next=/rocketchat/redirect
 - **URL API**: http://localhost:8000/rocketchat/api


Roadmap
-------

- Enforce unique email registration in Django admin, since Rocket.Chat requires this.
- Update Rocket.Chat user details in MongoDB when the user is modified in Django Admin.

.. _`Rocket.Chat`: https://github.com/RocketChat/Rocket.Chat) users using [Django framework](https://github.com/django/django
.. _`Rocket.Chat IFrame authentication`: https://rocket.chat/docs/administrator-guides/authentication/iframe/
.. _`django-cors-headers`: https://github.com/ottoyiu/django-cors-headers
.. _`Get an Rocket.Chat authentication token`: https://rocket.chat/docs/developer-guides/rest-api/authentication/login/
