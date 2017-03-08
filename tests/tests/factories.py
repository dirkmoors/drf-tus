# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import factory

from rest_framework_tus.models import get_upload_model


class UploadFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_upload_model()
