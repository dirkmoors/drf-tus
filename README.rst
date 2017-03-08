=============================
drf-tus
=============================

.. image:: https://badge.fury.io/py/drf-tus.svg
    :target: https://badge.fury.io/py/drf-tus

.. image:: https://travis-ci.org/dirkmoors/drf-tus.svg?branch=master
    :target: https://travis-ci.org/dirkmoors/drf-tus

.. image:: https://codecov.io/gh/dirkmoors/drf-tus/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dirkmoors/drf-tus

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
        'rest_framework_tus.apps.RestFrameworkTusConfig',
        ...
    )

Add drf-tus's URL patterns:

.. code-block:: python

    from rest_framework_tus import urls as rest_framework_tus_urls


    urlpatterns = [
        ...
        url(r'^', include(rest_framework_tus_urls)),
        ...
    ]

Features
--------

* TODO

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
