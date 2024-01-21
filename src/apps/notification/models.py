from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.db import models

from apps.core.models import BaseModel
from .enums import NotificationTypes

User = get_user_model()


# Notification model
class Notification(BaseModel):
    TYPES = NotificationTypes

    type = models.CharField(_('Notif type'), max_length=128, choices=TYPES.choices)
    title = models.CharField(_('Notif title'), max_length=255)
    description = models.TextField(_('Notif description'), null=True, blank=True)

    # Attach content
    image = models.ImageField(upload_to='images/notifications/', null=True, blank=True, max_length=512)
    kwargs = models.JSONField(_('KeyWord args'), null=True, blank=True)

    send_notify = models.BooleanField(_('Send Notify'), default=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('To user'), related_name='notifications')

    is_showing = models.BooleanField(_('Is showing'), default=True)  # Showing user or not

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ('-id',)

    def __str__(self):
        return f'Notification for {self.to_user}'

    def get_title(self):
        return self.title or 'notification'

    def get_content(self):
        return f"""
            {self.get_title()}
            {self.description}
        """

    def get_link(self):
        try:
            return self.kwargs['link']
        except KeyError:
            return ''

    def get_image_url(self):
        if self.image:
            return self.image.url
