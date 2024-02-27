from django.apps import AppConfig


class RestFrameworkTusConfig(AppConfig):
    name = "rest_framework_tus"

    default_auto_field = "django.db.models.BigAutoField"

    # noinspection PyUnresolvedReferences
    def ready(self):
        # Import receivers
        from . import receivers
