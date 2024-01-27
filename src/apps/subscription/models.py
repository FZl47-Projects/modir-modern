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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', verbose_name=_('User'))
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, related_name='subscribers', verbose_name=_('Subscription'), null=True)
    expire_date = models.DateField(_('Expire date'), null=True, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user} - {self.subscription}'

    def save(self, *args, **kwargs):
        if not self.expire_date:
            self.expire_date = datetime.now().date() + timedelta(int(self.subscription.type * 30))
        super().save(*args, **kwargs)

    def get_expire_date(self):
        return self.expire_date.strftime('%Y-%m-%d') or ''
