# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import json

from django.http import Http404
from django.urls.base import reverse

from rest_framework import mixins, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.metadata import BaseMetadata
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_framework_tus import constants, signals, states
from rest_framework_tus.exceptions import Conflict
from rest_framework_tus.serializers import UploadSerializer
from rest_framework_tus.utils import encode_upload_metadata, get_or_create_temp_file
from . import tus_api_version, tus_api_version_supported, tus_api_extensions, settings as tus_settings
from .models import get_upload_model

logger = logging.getLogger(__name__)


class UploadMetadata(BaseMetadata):
    def determine_metadata(self, request, view):
        return {
            'Tus-Resumable': tus_api_version,
            'Tus-Version': ','.join(tus_api_version_supported),
            'Tus-Extension': ','.join(tus_api_extensions),
            'Tus-Max-Size': tus_settings.TUS_MAX_FILE_SIZE,
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'PATCH,HEAD,GET,POST,OPTIONS',
            'Access-Control-Expose-Headers': 'Tus-Resumable,upload-length,upload-metadata,Location,Upload-Offset',
            'Access-Control-Allow-Headers':
                'Tus-Resumable,upload-length,upload-metadata,Location,Upload-Offset,content-type',
            'Cache-Control': 'no-store'
        }


class TusHeadMixin(object):
    def info(self, request, *args, **kwargs):
        try:
            upload = self.get_object()
        except Http404:
            # Instead of simply trowing a 404, we need to add a cache-control header to the response
            return Response('Not found.', headers={'Cache-Control': 'no-store'}, status=status.HTTP_404_NOT_FOUND)

        headers = {
            'Upload-Offset': upload.upload_offset,
            'Cache-Control': 'no-store'
        }

        if upload.upload_length >= 0:
            headers['Upload-Length'] = upload.upload_length

        if upload.upload_metadata:
            headers['Upload-Metadata'] = encode_upload_metadata(json.loads(upload.upload_metadata))

        return Response(headers=headers, status=status.HTTP_200_OK)


class TusCreateMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        # Get file size from request
        upload_length = getattr(request, constants.UPLOAD_LENGTH_FIELD_NAME, -1)

        # Validate upload_length
        if upload_length > tus_settings.TUS_MAX_FILE_SIZE:
            return Response('Invalid "Upload-Length". Maximum value: {}.'.format(tus_settings.TUS_MAX_FILE_SIZE),
                            status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        # If filesize is not given, we expect the defer header!
        if not upload_length or upload_length < 0:
            if getattr(request, constants.UPLOAD_DEFER_LENGTH_FIELD_NAME, -1) != 1:
                return Response('Missing "{Upload-Defer-Length}" header.', status=status.HTTP_400_BAD_REQUEST)

        # Get metadata from request
        upload_metadata = getattr(request, constants.UPLOAD_METADATA_FIELD_NAME, {})

        # Get data from metadata
        filename = upload_metadata.get('filename', '')

        # Create upload object
        upload = get_upload_model().objects.create(
            upload_length=upload_length, upload_metadata=json.dumps(upload_metadata), filename=filename)

        # Prepare response headers
        headers = {
            'Location': reverse('rest_framework_tus:api:upload-detail', kwargs={'guid': upload.guid}),
        }

        return Response(headers=headers, status=status.HTTP_201_CREATED)


class TusPatchMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed

    def partial_update(self, request, *args, **kwargs):
        # Validate content type
        self.validate_content_type(request)

        # Retrieve object
        upload = self.get_object()

        # Get upload_offset
        upload_offset = getattr(request, constants.UPLOAD_OFFSET_NAME)

        # Validate upload_offset
        if upload_offset != upload.upload_offset:
            raise Conflict

        # Make sure there is a tempfile for the upload
        get_or_create_temp_file(upload)

        # Change state
        if upload.state == states.INITIAL:
            upload.start_receiving()
            upload.save()

        # Write file
        chunk_size = int(request.META.get('CONTENT_LENGTH', 102400))
        try:
            upload.write_data(request.body, chunk_size)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        headers = {
            'Upload-Offset': upload.upload_offset,
        }

        if upload.upload_length == upload.upload_offset:
            # Trigger signal
            signals.received.send(sender=upload.__class__, instance=upload)

        return Response(headers=headers, status=status.HTTP_204_NO_CONTENT)

    @classmethod
    def validate_content_type(cls, request):
        content_type = request.META.get('headers', {}).get('Content-Type', '')

        if not content_type or content_type != 'application/upload_offset+octet-stream':
            return Response(
                'Invalid value for "Content-Type" header: {}. Expected "application/upload_offset+octet-stream".'
                    .format(content_type), status=status.HTTP_400_BAD_REQUEST)


class UploadViewSet(TusCreateMixin,
                    TusPatchMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    TusHeadMixin,
                    GenericViewSet):
    serializer_class = UploadSerializer
    metadata_class = UploadMetadata
    lookup_field = 'guid'
    lookup_value_regex = '[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}'

    def get_queryset(self):
        return get_upload_model().objects.all()
