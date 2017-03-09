# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.http.response import HttpResponse

from rest_framework import status

from . import tus_api_version, constants
from .compat import decode_base64


class TusMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_request(self, request):
        # Parse tus client version
        self.parse_tus_version(request)

        # Parse upload length
        self.parse_upload_length(request)

        # Parse upload upload_offset
        self.parse_upload_offset(request)

        # Parse defer upload length
        self.parse_upload_defer_length(request)

        # Parse upload metadata
        self.parse_upload_metadata(request)

        # Parse upload checksum
        self.parse_upload_checksum(request)

    def process_response(self, request, response):
        if 'Tus-Resumable' not in response:
            response['Tus-Resumable'] = tus_api_version

        return response

    @classmethod
    def parse_tus_version(cls, request):
        tus_version = request.META.get('headers', {}).get('Tus-Resumable', None)

        if tus_version is None:
            return

        # Set upload length
        setattr(request, constants.TUS_RESUMABLE_FIELD_NAME, tus_version)

    @classmethod
    def parse_upload_defer_length(cls, request,):
        upload_defer_length = request.META.get('headers', {}).get('Upload-Defer-Length', None)

        if not upload_defer_length:
            return

        upload_defer_length = int(upload_defer_length)

        if upload_defer_length != 1:
            return HttpResponse('Invalid value for "Upload-Defer-Length" header: {}.'.format(upload_defer_length),
                                status=status.HTTP_400_BAD_REQUEST)

        # Set upload defer length
        setattr(request, constants.UPLOAD_DEFER_LENGTH_FIELD_NAME, upload_defer_length)

    @classmethod
    def parse_upload_offset(cls, request):
        upload_offset = request.META.get('headers', {}).get('Upload-Offset', None)

        if upload_offset is None:
            return

        # Set upload length
        setattr(request, constants.UPLOAD_OFFSET_NAME, int(upload_offset))

    @classmethod
    def parse_upload_length(cls, request):
        upload_length = request.META.get('headers', {}).get('Upload-Length', None)

        if upload_length is None:
            return

        # Set upload length
        setattr(request, constants.UPLOAD_LENGTH_FIELD_NAME, int(upload_length))

    @classmethod
    def parse_upload_checksum(cls, request):
        upload_checksum_header = request.META.get('headers', {}).get('Upload-Checksum', None)

        if upload_checksum_header is None:
            return

        upload_checksum = list(upload_checksum_header.split(' '))
        if len(upload_checksum) != 2:
            return HttpResponse('Invalid value for "Upload-Checksum" header: {}.'.format(upload_checksum_header),
                                status=status.HTTP_400_BAD_REQUEST)

        # Set upload checksum
        setattr(request, constants.UPLOAD_CHECKSUM_FIELD_NAME, upload_checksum)

    @classmethod
    def parse_upload_metadata(cls, request):
        upload_meta_header = request.META.get('headers', {}).get('Upload-Metadata', None)

        if upload_meta_header is None:
            return

        upload_metadata = {}

        for key_value_pair in upload_meta_header.split(','):
            # Trim whitespace
            key_value_pair = key_value_pair.strip()

            # Split key and value
            key, value = key_value_pair.split(' ')

            # Store data
            upload_metadata[key] = decode_base64(value.encode('utf-8')).decode('ascii')

        # Set upload_metadata
        setattr(request, constants.UPLOAD_METADATA_FIELD_NAME, upload_metadata)
