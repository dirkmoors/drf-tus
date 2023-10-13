import copy
import json
from datetime import timedelta

from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_tus import settings as tus_settings
from rest_framework_tus import states, tus_api_extensions, tus_api_version, tus_api_version_supported
from rest_framework_tus.compat import reverse
from rest_framework_tus.models import get_upload_model
from rest_framework_tus.utils import (
    create_checksum_header,
    encode_base64_to_string,
    encode_upload_metadata,
    read_bytes_from_field_file,
)
from tests.tests.factories import UploadFactory


class ViewTests(APITestCase):
    def test_options(self):
        # Perform request
        result = self.client.options(
            reverse("rest_framework_tus:api:upload-list"),
            headers={"Tus-Resumable": tus_api_version},
        )
        assert result.status_code == status.HTTP_200_OK

        # Validate response headers
        assert "Tus-Resumable" in result

        expected = {
            "Tus-Resumable": tus_api_version,
            "Tus-Version": ",".join(tus_api_version_supported),
            "Tus-Extension": ",".join(tus_api_extensions),
            "Tus-Max-Size": tus_settings.TUS_MAX_FILE_SIZE,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "PATCH,HEAD,GET,POST,OPTIONS",
            "Access-Control-Expose-Headers": "Tus-Resumable,Upload-Length,Upload-Metadata,Location,Upload-Offset",
            "Access-Control-Allow-Headers": "Tus-Resumable,Upload-Length,Upload-Metadata,Location,Upload-Offset,"
            "Content-Type",
            "Cache-Control": "no-store",
        }

        for key in expected:
            assert result.data[key] == expected[key]

    def test_head_incorrect_header(self):
        # Create upload
        upload = UploadFactory()

        # Perform request
        result = self.client.head(reverse("rest_framework_tus:api:upload-detail", kwargs={"guid": upload.guid}))
        assert result.status_code == status.HTTP_400_BAD_REQUEST

        # Validate response headers
        assert "Tus-Resumable" in result

    def test_head(self):
        # Create upload
        upload = UploadFactory(
            upload_metadata=json.dumps({"filename": "test_file.jpg"}),
            expires=timezone.now() + timedelta(hours=1),
        )

        # Perform request
        result = self.client.head(
            reverse("rest_framework_tus:api:upload-detail", kwargs={"guid": upload.guid}),
            headers={"Tus-Resumable": tus_api_version},
        )

        # Check status
        assert result.status_code == status.HTTP_200_OK

        # Validate response headers
        assert "Tus-Resumable" in result
        assert int(result["Upload-Offset"]) >= 0
        assert result["Upload-Metadata"] == "filename {}".format(encode_base64_to_string("test_file.jpg"))
        assert result["Upload-Expires"] is not None

    def test_create_without_length(self):
        # Prepare creation headers
        headers = {
            "Tus-Resumable": tus_api_version,
            "Upload-Metadata": encode_upload_metadata(
                {
                    "filename": "test_file.jpg",
                },
            ),
        }

        # Perform request
        result = self.client.post(reverse("rest_framework_tus:api:upload-list"), headers=headers)

        # Check status
        assert result.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_without_length_with_defer(self):
        # Prepare creation headers
        headers = {
            "Tus-Resumable": tus_api_version,
            "Upload-Defer-Length": 1,
            "Upload-Metadata": encode_upload_metadata(
                {
                    # Make sure non-ASCII characters are supported (regression)
                    "filename": "test_file_٩(-̮̮̃-̃)۶ ٩(●̮̮̃•̃)۶ ٩(͡๏̯͡๏)۶ ٩(-̮̮̃•̃).jpg",
                },
            ),
        }

        # Perform request
        result = self.client.post(reverse("rest_framework_tus:api:upload-list"), headers=headers)

        # Check status
        assert result.status_code == status.HTTP_201_CREATED

        # Retrieve upload
        upload = get_upload_model().objects.all().first()

        # Validate upload
        assert upload.upload_length == -1
        assert upload.filename == "test_file_٩(-̮̮̃-̃)۶ ٩(●̮̮̃•̃)۶ ٩(͡๏̯͡๏)۶ ٩(-̮̮̃•̃).jpg"

        # Validate response headers
        assert "Tus-Resumable" in result
        assert result["Location"].endswith(
            reverse("rest_framework_tus:api:upload-detail", kwargs={"guid": upload.guid}),
        )

    def test_create_too_big(self):
        # Prepare creation headers
        headers = {
            "Tus-Resumable": tus_api_version,
            "Upload-Length": tus_settings.TUS_MAX_FILE_SIZE + 1,
            "Upload-Metadata": encode_upload_metadata(
                {
                    "filename": "test_file.jpg",
                },
            ),
        }

        # Perform request
        result = self.client.post(reverse("rest_framework_tus:api:upload-list"), headers=headers)

        # Check status
        assert result.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    def test_create(self):
        # Prepare creation headers
        headers = {
            "Tus-Resumable": tus_api_version,
            "Upload-Length": 100,
            "Upload-Metadata": encode_upload_metadata(
                {
                    "filename": "test_file.jpg",
                },
            ),
        }

        # Perform request
        result = self.client.post(reverse("rest_framework_tus:api:upload-list"), headers=headers)

        # Check status
        assert result.status_code == status.HTTP_201_CREATED

        # Retrieve upload
        upload = get_upload_model().objects.all().first()

        # Validate upload
        assert upload.upload_length == 100
        assert upload.filename == "test_file.jpg"

        # Validate response headers
        assert "Tus-Resumable" in result
        assert result["Location"].endswith(
            reverse("rest_framework_tus:api:upload-detail", kwargs={"guid": upload.guid}),
        )

    def test_terminate_while_saving(self):
        # Create upload
        upload = UploadFactory(
            filename="test_data.txt",
            upload_metadata=json.dumps({"filename": "test_data.txt"}),
            upload_length=100,
            state=states.SAVING,
        )

        # Prepare headers
        headers = {
            "Tus-Resumable": tus_api_version,
        }

        # Perform request
        result = self.client.delete(
            reverse("rest_framework_tus:api:upload-detail", kwargs={"guid": upload.guid}),
            headers=headers,
        )

        # Check result
        assert result.status_code == status.HTTP_409_CONFLICT

        # Verify existence
        assert get_upload_model().objects.filter(guid=upload.guid).exists()

    def test_terminate(self):
        # Create upload
        upload = UploadFactory(
            filename="test_data.txt",
            upload_metadata=json.dumps({"filename": "test_data.txt"}),
            upload_length=100,
            state=states.DONE,
        )

        # Prepare headers
        headers = {
            "Tus-Resumable": tus_api_version,
        }

        # Perform request
        result = self.client.delete(
            reverse("rest_framework_tus:api:upload-detail", kwargs={"guid": upload.guid}),
            headers=headers,
        )

        # Check result
        assert result.status_code == status.HTTP_204_NO_CONTENT

        # Verify existence
        assert get_upload_model().objects.filter(guid=upload.guid).exists() is False

    def test_upload_without_checksum(self):
        self._test_upload_with_checksum(None)

    def test_upload_with_md5_checksum(self):
        self._test_upload_with_checksum("md5")

    def test_upload_with_sha1_checksum(self):
        self._test_upload_with_checksum("sha1")

    def test_upload_with_sha224_checksum(self):
        self._test_upload_with_checksum("sha224")

    def test_upload_with_sha256_checksum(self):
        self._test_upload_with_checksum("sha256")

    def test_upload_with_sha384_checksum(self):
        self._test_upload_with_checksum("sha384")

    def test_upload_with_sha512_checksum(self):
        self._test_upload_with_checksum("sha512")

    def test_upload_with_unsupported_checksum(self):
        self._test_upload_with_checksum("ripemd160", expected_failure=status.HTTP_400_BAD_REQUEST)

    def test_upload_with_mismatching_checksum(self):
        self._test_upload_with_checksum("md5", checksum="md5 blabla", expected_failure=460)

    def _test_upload_with_checksum(self, checksum_algorithm, checksum=None, expected_failure=None):
        # Define blob
        blob = "Şởოè śấოρļể ẮŞĈİĪ-ŧểхŧ".encode()  # Make sure the data are **BYTES**!!!!

        # Create test data
        test_data = ("test_data.txt", blob)

        # Create upload
        upload = UploadFactory(
            filename=test_data[0],
            upload_metadata=json.dumps({"filename": test_data[0]}),
            upload_length=len(test_data[1]),
        )

        # Define chunk size
        chunk_size = 4  # 4 bytes

        # Write
        upload_offset = 0
        data = copy.copy(test_data[1])
        while True:
            # Take chunk
            chunk = data[:chunk_size]

            # Prepare headers
            headers = {
                "Tus-Resumable": tus_api_version,
                "Upload-Offset": upload_offset,
            }

            # Prepare checksum
            if checksum_algorithm is not None:
                try:
                    headers["Upload-Checksum"] = checksum or create_checksum_header(chunk, checksum_algorithm)
                except ValueError:
                    # Invalid checksum because algorithm is not supported by Python version
                    headers["Upload-Checksum"] = f"{checksum_algorithm} blablabla"

            # Perform request
            result = self.client.patch(
                reverse("rest_framework_tus:api:upload-detail", kwargs={"guid": upload.guid}),
                data=chunk,
                headers=headers,
                content_type="application/offset+octet-stream",
            )

            # Maybe we expect a failure
            if expected_failure:
                assert result.status_code == expected_failure

                # Cleanup file
                upload.delete()

                # The test is over here!
                return

            # Check result
            assert result.status_code == status.HTTP_204_NO_CONTENT

            # Update data
            data = data[chunk_size:]

            # Update iterator
            upload_offset += len(chunk)

            # Check final piece
            if upload_offset == len(test_data[1]):
                break

        # Reload upload
        upload = get_upload_model().objects.get(guid=upload.guid)

        # Assert file is ready
        assert upload.state == states.DONE

        # Compare data
        uploaded_data = read_bytes_from_field_file(upload.uploaded_file.file)
        assert uploaded_data == blob

        # Cleanup file
        upload.delete()
