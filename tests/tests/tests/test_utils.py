from unittest.case import TestCase

from rest_framework_tus.compat import decode_base64
from rest_framework_tus.utils import encode_base64_to_string, encode_upload_metadata


class UtilsTest(TestCase):
    def test_encode_64(self):
        data = b"filename123.jpg"

        # Encode
        result = encode_base64_to_string(data)

        # Decode
        initial = decode_base64(result.encode("utf-8"))

        assert initial == data

    def test_encode_upload_metadata(self):
        data = {
            "filename": "bla.jpg",
            "some-key": "hello.png",
        }

        # Encode!
        result = encode_upload_metadata(data)

        # Check result
        assert result == "filename {},some-key {}".format(
            encode_base64_to_string("bla.jpg"),
            encode_base64_to_string("hello.png"),
        )
