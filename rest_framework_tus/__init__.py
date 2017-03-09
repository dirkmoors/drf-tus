# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
default_app_config = 'rest_framework_tus.apps.RestFrameworkTusConfig'

__version__ = '1.2'

tus_api_version = '1.0.0'
tus_api_version_supported = ['1.0.0']
tus_api_extensions = ['creation', 'creation-defer-length', 'termination', 'checksum', 'expiration']
tus_api_checksum_algorithms = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']
