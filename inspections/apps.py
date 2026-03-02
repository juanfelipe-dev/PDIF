from django.apps import AppConfig


class InspectionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inspections'

    def ready(self):
        # import signals to connect them
        from . import signals  # noqa: F401
