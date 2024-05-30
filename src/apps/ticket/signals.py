from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notification.utils import create_notify_for_admins
from apps.notification.models import Notification
from . import models


@receiver(post_save, sender=models.Ticket)
def handle_new_ticket_notify(sender, instance, created, **kwargs):
    if created:
        # create for user
        Notification.objects.create(
            type='NEW_TICKET_CREATED',
            to_user=instance.user,
            title=_('New Ticket Submited')
        )
        # create for admin's
        create_notify_for_admins('NEW_TICKET_CREATED_ADMIN', _('New Ticket Submited'))
