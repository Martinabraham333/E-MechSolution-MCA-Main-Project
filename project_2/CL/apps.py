from django.apps import AppConfig


class ClConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CL'
    def ready(self):
        import CL.signals
