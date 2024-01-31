from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.db import models

from apps.core.models import BaseModel
User = get_user_model()


# MyRestaurant model
class Restaurant(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants', verbose_name=_('User'))
    title = models.CharField(_('Title'), max_length=128, default=_('No title'))
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Restaurant')
        verbose_name_plural = _('Restaurants')

    def __str__(self):
        return f'{self.user} - {self.title}'

    def get_material_categories(self):
        return self.raw_material_categories.filter(is_active=True)


# RawMaterialCategories model
class RawMaterialCategory(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='raw_material_categories', verbose_name=_('Restaurant'))
    title = models.CharField(_('Title'), max_length=128, default=_('Test category'))
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Raw materials category')
        verbose_name_plural = _('Raw materials categories')

    def __str__(self):
        return f'{self.restaurant} - {self.title}'
