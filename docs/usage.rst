=====
Usage
=====

To use drf-tus in a project, add it to your `INSTALLED_APPS`:

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
