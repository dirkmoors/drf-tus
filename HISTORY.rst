.. :changelog:

History
-------

2.0.1 (2023-10-13)
++++++++++++++++++

* Repair CI and tests.

2.0.0 (2023-07-06)
++++++++++++++++++

* Django 4.2 LTS compatibility.

1.21.2 (2018-09-04)
+++++++++++++++++++

* Fixed Django compatibility.

1.21.1 (2018-08-01)
+++++++++++++++++++

* Fixed failing travis build.

1.21 (2018-08-01)
+++++++++++++++++

* Updated Django dependency and dropped support for Python 3.3.x (https://github.com/dirkmoors/drf-tus/pull/9).

1.20 (2018-02-12)
+++++++++++++++++

* Implemented per-view max file size setting (https://github.com/dirkmoors/drf-tus/pull/8).

1.19 (2018-02-08)
+++++++++++++++++

* Fixed bug that occurred when pausing uploads (https://github.com/dirkmoors/drf-tus/pull/7).

1.18 (2018-02-08)
+++++++++++++++++

* Make the metadata 'filename' key a setting. (https://github.com/dirkmoors/drf-tus/pull/2).
* Switch from (Positive)IntegerField to BigIntegerField for the upload_length and upload_offset fields (https://github.com/dirkmoors/drf-tus/pull/3).
* Increase Django version support up to 1.11 (https://github.com/dirkmoors/drf-tus/pull/4).
* Fix unicode errors (https://github.com/dirkmoors/drf-tus/pull/5).
* Updated travis configuration.

1.17 (2017-05-10)
+++++++++++++++++

* Exchanged use of `base64.encodebytes` to `base64.b64encode`.

1.16 (2017-05-04)
+++++++++++++++++

* Implemented `validate_filename` handler in `TusCreateMixin`.

1.15 (2017-04-06)
+++++++++++++++++

* Added missing migration and changed max_length to 255 for model `Upload`'s attribute `uploaded_file`.

1.14 (2017-03-30)
+++++++++++++++++

* Updated default behaviour of the `get_header` handler in `TusMiddleware`.

1.13 (2017-03-30)
+++++++++++++++++

* Implemented handler for retrieving request headers in `TusMiddleware`.

1.12 (2017-03-10)
+++++++++++++++++

* Updated `validate_chunk` signature.

1.11 (2017-03-10)
+++++++++++++++++

* Implemented `validate_chunk` handler method in TusPatchMixin.
* Implemented `validate_success_headers` handler method in TusCreateMixin.

1.10 (2017-03-09)
+++++++++++++++++

* Disabled chunk writing to disk.

1.9 (2017-03-09)
++++++++++++++++

* Introduced TusUploadStreamParser.

1.8 (2017-03-09)
++++++++++++++++

* Introduced setting to include serializer data in response body.

1.7 (2017-03-09)
++++++++++++++++

* Bugfixes.

1.6 (2017-03-09)
++++++++++++++++

* Bugfixes.

1.5 (2017-03-09)
++++++++++++++++

* Updated middleware, removed required header (bug!).

1.4 (2017-03-09)
++++++++++++++++

* Initial migration.

1.3 (2017-03-09)
++++++++++++++++

* Renamed some parameters / classes.

1.2 (2017-03-09)
++++++++++++++++

* Cleanup repository.


1.1 (2017-03-09)
++++++++++++++++

* First release on PyPI.
