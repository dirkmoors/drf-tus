# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections
import os
import tempfile
import uuid

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMField, transition
from jsonfield import JSONField

from rest_framework_tus import signals
from rest_framework_tus import states
from rest_framework_tus.utils import write_bytes_to_file


class AbstractUpload(models.Model):
    """
    Abstract model for managing TUS uploads
    """
    guid = models.UUIDField(_('GUID'), default=uuid.uuid4, unique=True)

    state = FSMField(default=states.INITIAL)

    upload_offset = models.BigIntegerField(default=0)
    upload_length = models.BigIntegerField(default=-1)

    upload_metadata = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})

    filename = models.CharField(max_length=255, blank=True)

    temporary_file_path = models.CharField(max_length=4096, null=True)

    expires = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def clean_fields(self, exclude=None):
        super(AbstractUpload, self).clean_fields(exclude=exclude)
        if self.upload_offset < 0:
            raise ValidationError(_('upload_offset should be >= 0.'))

    def write_data(self, bytes, chunk_size):
        num_bytes_written = write_bytes_to_file(self.temporary_file_path, self.upload_offset, bytes, makedirs=True)

        if num_bytes_written > 0:
            self.upload_offset += num_bytes_written
            self.save()

    def delete(self, *args, **kwargs):
        if self.temporary_file_path and os.path.exists(self.temporary_file_path):
            os.remove(self.temporary_file_path)
        super(AbstractUpload, self).delete(*args, **kwargs)

    def generate_filename(self):
        return os.path.join('{}.bin'.format(uuid.uuid4()))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.filename:
            self.filename = self.generate_filename()
        return super(AbstractUpload, self).save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def is_complete(self):
        return self.upload_offset == self.upload_length

    def temporary_file_exists(self):
        return self.temporary_file_path and os.path.isfile(self.temporary_file_path)

    def _temporary_file_exists(self):
        return self.temporary_file_exists()

    def get_or_create_temporary_file(self):
        if not self.temporary_file_path:
            fd, path = tempfile.mkstemp(prefix="tus-upload-")
            os.close(fd)
            self.temporary_file_path = path
            self.save()
        assert os.path.isfile(self.temporary_file_path)
        return self.temporary_file_path

    @transition(field=state, source=states.INITIAL, target=states.RECEIVING, conditions=[_temporary_file_exists])
    def start_receiving(self):
        """
        State transition to indicate the first file chunk has been received successfully
        """
        # Trigger signal
        signals.receiving.send(sender=self.__class__, instance=self)

    @transition(field=state, source=states.RECEIVING, target=states.SAVING, conditions=[is_complete])
    def start_saving(self):
        """
        State transition to indicate that the upload is complete, and that the temporary file will be transferred to
          its final destination.
        """
        # Trigger signal
        signals.saving.send(sender=self.__class__, instance=self)

    @transition(field=state, source=states.SAVING, target=states.DONE)
    def finish(self):
        """
        State transition to indicate the upload is ready and the file is ready for access
        """
        # Trigger signal
        signals.finished.send(sender=self.__class__, instance=self)


class Upload(AbstractUpload):
    """
    Default Upload model
    """
    uploaded_file = models.FileField(upload_to='uploaded', blank=True, null=True, max_length=255)

    def delete(self, *args, **kwargs):
        if self.state == states.DONE:
            self.uploaded_file.delete()
        super(Upload, self).delete(*args, **kwargs)


def get_upload_model():
    """
    Returns the Upload model that is active in this project.
    """
    from django.apps import apps as django_apps
    from .settings import TUS_UPLOAD_MODEL
    try:
        return django_apps.get_model(TUS_UPLOAD_MODEL)
    except ValueError:
        raise ImproperlyConfigured('UPLOAD_MODEL must be of the form \'app_label.model_name\'')
    except LookupError:
        raise ImproperlyConfigured('UPLOAD_MODEL refers to model \'%s\' that has not been installed' % TUS_UPLOAD_MODEL)
