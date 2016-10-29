from django.apps import AppConfig


class DjAuthConfig(AppConfig):
    name = 'dj_auth'

    def ready(self):
        import dj_auth.signals
