# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings as django_settings

# Retrieve root settings dict
REST_FRAMEWORK_TUS = getattr(django_settings, 'REST_FRAMEWORK_TUS', {})


# Retrieve settings
TUS_UPLOAD_MODEL = REST_FRAMEWORK_TUS.get('UPLOAD_MODEL', 'rest_framework_tus.Upload')
# TUS_UPLOAD_ROOT = REST_FRAMEWORK_TUS.get('UPLOAD_ROOT', django_settings.MEDIA_ROOT)
TUS_UPLOAD_DIR = REST_FRAMEWORK_TUS.get('UPLOAD_DIR', os.path.join(django_settings.BASE_DIR, 'tmp/uploads/'))
TUS_SAVE_STRATEGY_CLASS = \
    REST_FRAMEWORK_TUS.get('SAVE_STRATEGY_CLASS', 'rest_framework_tus.storage.DefaultSaveStrategy')

# TUS_UPLOAD_URL = REST_FRAMEWORK_TUS.get('UPLOAD_URL', '/media')
# TUS_UPLOAD_DIR = REST_FRAMEWORK_TUS.get('UPLOAD_DIR', os.path.join(django_settings.BASE_DIR, 'tmp/uploads/'))
# TUS_DESTINATION_DIR = REST_FRAMEWORK_TUS.get('DESTINATION_DIR', django_settings.MEDIA_ROOT)
TUS_MAX_FILE_SIZE = REST_FRAMEWORK_TUS.get('MAX_FILE_SIZE', 4294967296)  # in bytes
TUS_FILE_OVERWRITE = REST_FRAMEWORK_TUS.get('FILE_OVERWRITE', True)
TUS_TIMEOUT = REST_FRAMEWORK_TUS.get('TIMEOUT', 3600)

