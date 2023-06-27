import factory

from rest_framework_tus.models import get_upload_model


class UploadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_upload_model()
