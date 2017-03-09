# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import base64
import copy
import tempfile
import hashlib


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


def read_bytes_from_field_file(field_file):
    try:
        field_file.open()
        result = field_file.read()
    finally:
        field_file.close()
    return result


def read_bytes(path):
    with open(path, 'r+b') as fh:
        result = fh.read()
    return result


def write_chunk_to_temp_file(bytes):
    chunk_file = create_temp_file_for_chunk()

    with open(chunk_file, 'wb') as fh:
        fh.write(bytes)

    return chunk_file


def create_temp_file_for_chunk():
    fd, path = tempfile.mkstemp(prefix="tus-upload-chunk-")
    os.close(fd)
    return path


def get_or_create_temp_file_for_upload(upload):
    if not upload.temporary_file_path:
        fd, path = tempfile.mkstemp(prefix="tus-upload-")
        os.close(fd)
        upload.temporary_file_path = path
        upload.save()
    assert os.path.isfile(upload.temporary_file_path)
    return upload.temporary_file_path


def create_checksum(bytes, checksum_algorithm):
    m = hashlib.new(checksum_algorithm)
    m.update(bytes)
    return m.hexdigest()


def pack_checksum(bytes, checksum_algorithm):
    checksum =create_checksum(bytes, checksum_algorithm)
    return '{checksum_algorithm} {checksum}'.format(checksum_algorithm=checksum_algorithm, checksum=checksum)


def is_correct_checksum_for_file(checksum_algorithm, checksum, file_path):
    bytes = read_bytes(file_path)
    bytes_checksum = create_checksum(bytes, checksum_algorithm)
    return bytes_checksum == checksum
