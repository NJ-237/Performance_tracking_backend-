from django.apps import AppConfig
# from . import signals

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'


    def ready(self):
        import authentication.signals  # Import your signals module