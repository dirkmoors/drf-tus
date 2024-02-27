from django.http.response import HttpResponse

from rest_framework import status

from . import constants, tus_api_version
from .compat import decode_base64


class TusMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        if hasattr(self, "process_request"):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, "process_response"):
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
        if "Tus-Resumable" not in response:
            response["Tus-Resumable"] = tus_api_version

        return response

    @classmethod
    def parse_tus_version(cls, request):
        tus_version = cls.get_header(request, "Tus-Resumable", None)

        if tus_version is None:
            return

        # Set upload length
        setattr(request, constants.TUS_RESUMABLE_FIELD_NAME, tus_version)

    @classmethod
    def parse_upload_defer_length(cls, request):
        upload_defer_length = cls.get_header(request, "Upload-Defer-Length", None)

        if not upload_defer_length:
            return

        upload_defer_length = int(upload_defer_length)

        if upload_defer_length != 1:
            return HttpResponse(
                f'Invalid value for "Upload-Defer-Length" header: {upload_defer_length}.',
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set upload defer length
        setattr(request, constants.UPLOAD_DEFER_LENGTH_FIELD_NAME, upload_defer_length)

    @classmethod
    def parse_upload_offset(cls, request):
        upload_offset = cls.get_header(request, "Upload-Offset", None)

        if upload_offset is None:
            return

        # Set upload length
        setattr(request, constants.UPLOAD_OFFSET_NAME, int(upload_offset))

    @classmethod
    def parse_upload_length(cls, request):
        upload_length = cls.get_header(request, "Upload-Length", None)

        if upload_length is None:
            return

        # Set upload length
        setattr(request, constants.UPLOAD_LENGTH_FIELD_NAME, int(upload_length))

    @classmethod
    def parse_upload_checksum(cls, request):
        upload_checksum_header = cls.get_header(request, "Upload-Checksum", None)

        if upload_checksum_header is None:
            return

        upload_checksum = list(upload_checksum_header.split(" "))
        if len(upload_checksum) != 2:
            return HttpResponse(
                f'Invalid value for "Upload-Checksum" header: {upload_checksum_header}.',
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set upload checksum
        setattr(request, constants.UPLOAD_CHECKSUM_FIELD_NAME, upload_checksum)

    @classmethod
    def parse_upload_metadata(cls, request):
        upload_meta_header = cls.get_header(request, "Upload-Metadata", None)

        if upload_meta_header is None:
            return

        upload_metadata = {}

        for key_value_pair in upload_meta_header.split(","):
            # Trim whitespace
            key_value_pair = key_value_pair.strip()

            # Split key and value
            key, value = key_value_pair.split(" ")

            # Store data
            upload_metadata[key] = decode_base64(value.encode("ascii")).decode("utf-8")

        # Set upload_metadata
        setattr(request, constants.UPLOAD_METADATA_FIELD_NAME, upload_metadata)

    @classmethod
    def get_header(cls, request, key, default_value=None):
        # First, we try to retrieve the key in the "headers" dictionary
        result = request.META.get("headers", {}).get(key, None)

        # If we didn't find the key, or the value was "None", try to use the "HTTP_{uppercased-key}" key
        if result is None:
            custom_value = "HTTP_{}".format(key.replace("-", "_").upper())
            result = request.META.get(custom_value, default_value)

        # If we didn't find the key, or the value was "None", try to use the "HTTP_X_{uppercased-key}" key
        if result is None:
            # https://tools.ietf.org/html/rfc6648
            custom_value = "HTTP_X_{}".format(key.replace("-", "_").upper())
            result = request.META.get(custom_value, default_value)

        # If we still didn't find the key, or the value was "None", return the default value
        if result is None:
            result = default_value

        # Return the result
        return result
