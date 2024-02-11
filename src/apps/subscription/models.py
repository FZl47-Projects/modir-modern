from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.db import models

from datetime import datetime, timedelta
from apps.core.models import BaseModel
from .enums import SubscriptionTypesEnum

User = get_user_model()


# Subscriptions model
class Subscription(BaseModel):
    Types = SubscriptionTypesEnum

    type = models.SmallIntegerField(_('Subscription type'), choices=Types.choices, unique=True)
    price = models.PositiveIntegerField(_('Price'), default=0)
    discount = models.PositiveIntegerField(_('Discount'), default=0)
    selling_price = models.PositiveIntegerField(_('Selling price'), default=0)
    promo = models.BooleanField(_('Promo'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self):
        return self.get_type_display()

    def save(self, *args, **kwargs):
        self.selling_price = int(self.price - (self.price * (self.discount / 100)))
        return super().save(*args, **kwargs)

    def get_type_label(self):
        return self.get_type_display()


# Subscribers model
class Subscriber(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription', verbose_name=_('User'))
    expire_date = models.DateField(_('Expire date'), null=True, blank=True)
    is_active = models.BooleanField(_('Active'), default=False)

    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user} - {self.get_expire_date()}'

    def add_time(self, subscription: Subscription):
        if self.is_active and self.expire_date:
            self.expire_date += timedelta(days=subscription.type * 30)
        else:
            self.expire_date = datetime.now() + timedelta(days=subscription.type * 30)
            self.is_active = True

        self.save()

    def get_expire_date(self):
        return self.expire_date.strftime('%Y-%m-%d') or ''
