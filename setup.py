#!/usr/bin/env python
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from rest_framework_tus/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("rest_framework_tus", "__init__.py")


if sys.argv[-1] == "publish":
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == "tag":
    print("Tagging the version on git:")
    os.system(f"git tag -a {version} -m 'version {version}'")
    os.system("git push --tags")
    sys.exit()

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")

setup(
    name="drf-tus",
    version=version,
    description="A Tus (tus.io) library for Django Rest Framework",
    long_description=f"{readme}\n\n{history}",
    author="Dirk Moors",
    author_email="dirkmoors@gmail.com",
    url="https://github.com/dirkmoors/drf-tus",
    packages=[
        "rest_framework_tus",
    ],
    include_package_data=True,
    install_requires=[
        "python-dateutil>=2.8.2",
        "Django>=3.2,<=4.2",
        "djangorestframework>=3.14.0",
        "jsonfield>=2.0.0",
        "django-fsm==2.8.1",
        "six>=1.11.0",
    ],
    license="MIT",
    zip_safe=False,
    keywords=[
        "drf-tus",
        "tus",
        "django",
        "rest",
        "framework",
        "django-rest-framework",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
