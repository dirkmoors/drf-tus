# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64

from unittest.case import TestCase

from rest_framework_tus.utils import encode_upload_metadata, encode_base64_to_string


class UtilsTest(TestCase):
    def test_encode_64(self):
        data = b'filename123.jpg'

        # Encode
        result = encode_base64_to_string(data)

        # Decode
        initial = base64.decodebytes(result.encode('utf-8'))

        assert initial == data

    def test_encode_upload_metadata(self):
        data = {
            'filename': 'bla.jpg',
            'some-key': 'hallo.png'
        }

        # Encode!
        result = encode_upload_metadata(data)

        # Check result
        assert result == 'filename {},some-key {}'.format(encode_base64_to_string('bla.jpg'), encode_base64_to_string('hallo.png'))