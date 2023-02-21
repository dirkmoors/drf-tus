# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod

from django.core.files import File
from six import with_metaclass

from django.utils.module_loading import import_string

from rest_framework_tus import signals
from .settings import TUS_SAVE_HANDLER_CLASS


class AbstractUploadSaveHandler(with_metaclass(ABCMeta, object)):
    def __init__(self, upload):
        self.upload = upload

    @abstractmethod
    def handle_save(self):
        pass

    def run(self):
        # Trigger state change
        self.upload.start_saving()
        self.upload.save()

        # Initialize saving
        self.handle_save()

    def finish(self):
        # Trigger signal
        signals.saved.send(sender=self.__class__, instance=self)

        # Finish
        self.upload.finish()
        self.upload.save()


class DefaultSaveHandler(AbstractUploadSaveHandler):
    destination_file_field = 'uploaded_file'

    def handle_save(self):
        # Save temporary field to file field
        file_field = getattr(self.upload, self.destination_file_field)
        file_field.save(self.upload.filename, File(open(self.upload.temporary_file_path, 'rb')))

        # Finish upload
        self.finish()


def get_save_handler(import_path=None):
    return import_string(import_path or TUS_SAVE_HANDLER_CLASS)
