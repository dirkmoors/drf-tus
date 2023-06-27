=====
Usage
=====

To use drf-tus in a project, add it to your `INSTALLED_APPS`:

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
