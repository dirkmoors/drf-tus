import hashlib
import os
import sys
import tempfile

import six

from .compat import encode_base64


def encode_base64_to_string(data):
    """
    Helper to encode a string or bytes value to a base64 string as bytes

    :param six.text_types data:
    :return six.binary_type:
    """

    if not isinstance(data, bytes):
        if isinstance(data, str):
            data = data.encode("utf-8")
        else:
            data = str(data).encode("utf-8")

    return encode_base64(data).decode("ascii").rstrip("\n")


def encode_upload_metadata(upload_metadata):
    """
    Encodes upload metadata according to the TUS 1.0.0 spec (http://tus.io/protocols/resumable-upload.html#creation)

    :param dict upload_metadata:
    :return str:
    """
    # Prepare encoded data
    encoded_data = [
        (key, encode_base64_to_string(value))
        for (key, value) in sorted(upload_metadata.items(), key=lambda item: item[0])
    ]

    # Encode into string
    return ",".join([" ".join([key, encoded_value]) for key, encoded_value in encoded_data])


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

    num_bytes_written = -1

    fh = None
    try:
        try:
            fh = open(file_path, "r+b")
        except OSError:
            fh = open(file_path, "wb")
        fh.seek(offset, os.SEEK_SET)
        num_bytes_written = fh.write(bytes)
    finally:
        if fh is not None:
            fh.close()

    # For python version < 3, "fh.write" will return None...
    if sys.version_info[0] < 3:
        num_bytes_written = len(bytes)

    return num_bytes_written


def read_bytes_from_field_file(field_file):
    """
    Returns the bytes read from a FieldFile

    :param ~django.db.models.fields.files.FieldFile field_file:
    :return six.binary_type: bytes read from the given field_file
    """
    try:
        field_file.open()
        result = field_file.read()
    finally:
        field_file.close()
    return result


def read_bytes(path):
    """
    Returns the bytes read from a local file at the given path

    :param str path: The local path to the file to read
    :return six.binary_type: bytes read from the given field_file
    """
    with open(path, "r+b") as fh:
        result = fh.read()
    return result


def write_chunk_to_temp_file(bytes):
    """
    Write some bytes to a local temporary file and return the path

    :param six.binary_type bytes: The bytes to write
    :return str: The local path to the temporary file that has been written
    """
    fd, chunk_file = tempfile.mkstemp(prefix="tus-upload-chunk-")
    os.close(fd)

    with open(chunk_file, "wb") as fh:
        fh.write(bytes)

    return chunk_file


def create_checksum(bytes, checksum_algorithm):
    """
    Create a hex-checksum for the given bytes using the given algorithm

    :param six.binary_type bytes: The bytes to create the checksum for
    :param str checksum_algorithm: The algorithm to use (e.g. "md5")
    :return str: The checksum (hex)
    """
    m = hashlib.new(checksum_algorithm)
    m.update(bytes)
    return m.hexdigest()


def create_checksum_header(bytes, checksum_algorithm):
    """
    Creates a hex-checksum header for the given bytes using the given algorithm

    :param six.binary_type bytes: The bytes to create the checksum for
    :param str checksum_algorithm: The algorithm to use (e.g. "md5")
    :return str: The checksum algorithm, followed by the checksum (hex)
    """
    checksum = create_checksum(bytes, checksum_algorithm)
    return f"{checksum_algorithm} {checksum}"


def checksum_matches(checksum_algorithm, checksum, bytes):
    """
    Checks if the given checksum matches the checksum for the data in the file

    :param str checksum_algorithm: The checksum algorithm to use
    :param str checksum: The original hex-checksum to match against
    :param six.binary_type bytes: The bytes to check
    :return bool: Whether or not the newly calculated checksum matches the given checksum
    """
    bytes_checksum = create_checksum(bytes, checksum_algorithm)
    return bytes_checksum == checksum
