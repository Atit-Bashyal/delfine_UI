import sys
from django.apps import AppConfig
from django.conf import settings


class IndeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indeed'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        from .training_schedule import training_updater
        if settings.SCHEDULER_AUTOSTART:
            training_updater.start()
