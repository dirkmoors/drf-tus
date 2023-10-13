import os

import django

DEBUG = True
USE_TZ = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "_yob+z9_*2zt@g=uv5rfbp^fky0^$2x&$3%6#)(g294h##ndmb"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "rest_framework_tus",
]

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ("rest_framework_tus.middleware.TusMiddleware",)
else:
    MIDDLEWARE_CLASSES = ("rest_framework_tus.middleware.TusMiddleware",)
