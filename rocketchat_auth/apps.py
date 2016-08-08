from django.apps import AppConfig


class RocketchatAuthConfig(AppConfig):
    name = 'rocketchat_auth'

    def ready(self):
        import rocketchat_auth.signals  # noqa
