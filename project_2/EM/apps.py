from django.apps import AppConfig


class EmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EM'

    def ready(self):
        import EM.signals
