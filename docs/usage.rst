=====
Usage
=====

To use drf-tus in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'rest_framework_tus',
        ...
    )

Add the middleware to `MIDDLEWARE` (or `MIDDLEWARE_CLASSES` for Django < 1.10)

.. code-block:: python

    MIDDLEWARE = (
        ...
        'rest_framework_tus.middleware.TusMiddleware',
        ...
    )

Add drf-tus's URL patterns:

.. code-block:: python

    urlpatterns = [
        ...
        url(r'^', include('rest_framework_tus.urls', namespace='rest_framework_tus')),
        ...
    ]
