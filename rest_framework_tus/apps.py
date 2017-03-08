# -*- coding: utf-8
from django.apps import AppConfig


class RestFrameworkTusConfig(AppConfig):
    name = 'rest_framework_tus'

    # noinspection PyUnresolvedReferences
    def ready(self):
        # Import receivers
        from . import receivers
