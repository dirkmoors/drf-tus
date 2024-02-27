from rest_framework import serializers

from rest_framework_tus.models import get_upload_model


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_upload_model()
        fields = "__all__"
