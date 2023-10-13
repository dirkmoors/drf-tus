import logging

from django.dispatch import receiver

from rest_framework_tus.models import get_upload_model
from rest_framework_tus.signals import finished, received, saved
from rest_framework_tus.storage import get_save_handler

logger = logging.getLogger(__name__)


@receiver(received, sender=get_upload_model())
def on_receiving_done(sender, instance, **kwargs):
    logger.debug(f"on_receiving_done: {instance}")
    save_handler = get_save_handler()
    save_handler(upload=instance).run()


@receiver(saved, sender=get_upload_model())
def on_saving_done(sender, instance, **kwargs):
    logger.debug(f"on_saving_done: {instance}")


@receiver(finished, sender=get_upload_model())
def on_finished(sender, instance, **kwargs):
    logger.debug(f"on_finished: {instance}")
