# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import base64
import copy
import tempfile


def encode_base64_to_string(string_value):
    data = copy.copy(string_value)

    if not isinstance(data, bytes):
        if isinstance(data, str):
            data = data.encode('utf-8')
        else:
            data = str(data).encode('utf-8')

    return base64.encodebytes(data).decode('ascii').rstrip('\n')


def encode_upload_metadata(upload_metadata):
    """
    Encodes upload metadata according to the TUS 1.0.0 spec (http://tus.io/protocols/resumable-upload.html#creation)

    :param dict upload_metadata:
    :return:
    """
    # Prepare encoded data
    encoded_data = [(key, encode_base64_to_string(value))
                    for (key, value) in sorted(upload_metadata.items(), key=lambda item: item[0])]

    # Encode into string
    return ','.join([' '.join([key, encoded_value]) for key, encoded_value in encoded_data])


def write_bytes_to_file(file_path, offset, bytes, makedirs=False):
    """
    Util to write bytes to a local file at a specific offset

    :param str file_path:
    :param int offset:
    :param six.binary_type bytes:
    :param bool makedirs: Whether or not to create the file_path's directories if they don't exist
    :return int: The amount of bytes written
    """
    if makedirs:
        if not os.path.isdir(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

    fh = None
    try:
        try:
            fh = open(file_path, 'r+b')
        except IOError:
            fh = open(file_path, 'wb')
        fh.seek(offset, os.SEEK_SET)
        fh.write(bytes)
    finally:
        if fh is not None:
            fh.close()

    return len(bytes)


def get_or_create_temp_file(upload):
    if not upload.temporary_file_path:
        fd, path = tempfile.mkstemp(prefix="tus-upload-part-")
        os.close(fd)
        upload.temporary_file_path = path
        upload.save()
    assert os.path.isfile(upload.temporary_file_path)
    return upload.temporary_file_path