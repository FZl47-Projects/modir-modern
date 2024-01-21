from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification
from . import sms


def sms_notify_handler(notification, phone_number):
    """ Handle sms config based on notification type """
    handler_pattern = sms.NOTIFICATION_USER_HANDLERS.get(notification.type, None)

    if handler_pattern:
        handler_pattern(notification, phone_number)


@receiver(post_save, sender=Notification)
def handle_notification_user_notify(sender, instance, **kwargs):
    if instance.send_notify:
        user = instance.to_user
        phone_number = user.phone_number

        if phone_number:
            sms_notify_handler(instance, phone_number)
