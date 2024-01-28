from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.db import models

from .enums import TicketTypesEnum, TicketStatusEnum
from .utils import ticket_file_src
User = get_user_model()


# Tickets model
class Ticket(models.Model):
    Types = TicketTypesEnum
    Status = TicketStatusEnum

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tickets', verbose_name=_('User'), null=True)
    title = models.CharField(_('Title'), max_length=128, default=_('No title'))
    type = models.CharField(_('Type'), max_length=64, choices=Types.choices, default=Types.GENERAL)
    status = models.CharField(_('Status'), max_length=32, choices=Status.choices, default=Status.OPEN)
    is_active = models.BooleanField(_('Active'), default=True)

    created_at = models.DateTimeField(_('Creation time'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Update time'), auto_now=True)

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.title} - {self.user}'

    def get_created_date(self):
        return self.created_at.strftime('%Y-%m-%d')

    def get_type_label(self):
        return self.get_type_display()

    def get_messages(self):
        return self.messages.all()

    def get_absolute_url(self):
        return reverse('ticket:ticket_details', args=[self.pk])


# Ticket Messages model
class Messages(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages', verbose_name=_('Ticket'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='ticket_messages', verbose_name=_('User'), null=True)
    text = models.TextField(_('Text'), max_length=512)
    file = models.FileField(_('Related file'), upload_to=ticket_file_src, null=True, blank=True)

    created_at = models.DateTimeField(_('Creation time'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Update time'), auto_now=True)

    class Meta:
        verbose_name = _('Ticket message')
        verbose_name_plural = _('Ticket messages')

    def __str__(self):
        return f'{self.ticket}'

    def get_created_date(self):
        return self.created_at.strftime('%Y-%m-%d')
