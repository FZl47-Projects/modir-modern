from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.db import models

from apps.core.models import BaseModel
User = get_user_model()


# Orders model
class Order(BaseModel):
    oid = models.PositiveBigIntegerField(_('Order ID'), null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', verbose_name=_('User'), null=True, blank=True)
    payable_price = models.IntegerField(_('Payable price'), default=0)
    discount_price = models.IntegerField(_('Discount price'), default=0)
    bank_tracking_code = models.CharField(_('Bank tracking code'), max_length=128, default='NA')

    callback_url = models.URLField(_('Callback url'), max_length=255, null=True, blank=True, editable=False)
    
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{self.user} - {self.user.profile.place_name} - {self.oid}'

    def create_oid(self):
        self.oid = int(self.id + 100)
        self.save()


# OrderItems model
class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))

    item_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item_object = GenericForeignKey('item_type', 'object_id')

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')
