=============================
drf-tus
=============================

.. image:: https://badge.fury.io/py/drf-tus.svg
    :target: https://badge.fury.io/py/drf-tus

.. image:: https://github.com/dirkmoors/drf-tus/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/dirkmoors/drf-tus/actions

A Tus (tus.io) library for Django Rest Framework

Documentation
-------------

The full documentation is at https://drf-tus.readthedocs.io.

Quickstart
----------

Install drf-tus::

    pip install drf-tus

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        "rest_framework_tus",
        ...
    )

Add the middleware to `MIDDLEWARE`:

.. code-block:: python

    MIDDLEWARE = (
        ...
        "rest_framework_tus.middleware.TusMiddleware",
        ...
    )

Add URL patterns for drf-tus:

.. code-block:: python

    urlpatterns = [
        ...
        path(r"^", include("rest_framework_tus.urls", namespace="rest_framework_tus")),
        ...
    ]

Features
--------

This library implements the following TUS API v1.0.0 protocols:

* Core Protocol (http://tus.io/protocols/resumable-upload.html#core-protocol)
* Creation Protocol (http://tus.io/protocols/resumable-upload.html#creation)
* Expiration Protocol (http://tus.io/protocols/resumable-upload.html#expiration)
* Checksum Protocol (http://tus.io/protocols/resumable-upload.html#checksum)
* Termination Protocol (http://tus.io/protocols/resumable-upload.html#termination)

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
