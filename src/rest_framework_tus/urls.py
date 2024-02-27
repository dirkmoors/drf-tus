from django.urls import include, path

from rest_framework_tus.views import UploadViewSet

from .routers import TusAPIRouter

app_name = "rest_framework_tus"

router = TusAPIRouter()
router.register(r"files", UploadViewSet, basename="upload")

urlpatterns = [
    path(r"", include((router.urls, "rest_framework_tus"), namespace="api")),
]
