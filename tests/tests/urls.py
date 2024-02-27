from django.urls import include, path

from rest_framework_tus.urls import urlpatterns as rest_framework_tus_urlpatterns

urlpatterns = [
    path(r"", include((rest_framework_tus_urlpatterns, "rest_framework_tus"), namespace="api")),
]
