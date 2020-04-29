# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework_tus.views import UploadViewSet

from .routers import TusAPIRouter

router = TusAPIRouter()
router.register(r'files', UploadViewSet, basename='upload')

urlpatterns = [
    url(r'', include((router.urls, 'rest_framework_tus'), namespace='api'))
]
app_name = 'rest_framework_tus'
