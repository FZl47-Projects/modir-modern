from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
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
        return f'{self.user} - {self.user.profile.place_name}'

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

    def get_materials(self):
        return self.raw_materials.all()


# RawMaterials model
class RawMaterial(BaseModel):
    category = models.ForeignKey(RawMaterialCategory, on_delete=models.CASCADE, related_name='raw_materials', verbose_name=_('Category'))

    # Common info
    title = models.CharField(_('Title'), max_length=128)
    price = models.PositiveIntegerField(_('Price'), default=0, help_text=_('Per unit'))
    use_for = models.CharField(_('Use for'), max_length=128, null=True, blank=True)
    quantity_raw_press = models.DecimalField(_('Standard quantity per raw press'), max_digits=5, decimal_places=3, default=0)
    quantity_baked_press = models.DecimalField(_('Standard quantity per baked press'), max_digits=5, decimal_places=3, default=0)
    delivery_weight = models.DecimalField(_('Delivery weight'), max_digits=5, decimal_places=2, default=0)

    # Weight loss during cleaning info
    weight_loss_cleaning_usable = models.DecimalField(_('Weight loss due to cleaning(usable)'), max_digits=4, decimal_places=2, default=0)
    weight_loss_cleaning_unusable = models.DecimalField(_('Weight loss due to cleaning(unusable)'), max_digits=4, decimal_places=2, default=0)
    edible_cleaned_weight = models.DecimalField(_('Edible cleaned weight'), max_digits=5, decimal_places=2, default=0)

    # Weight loss during baking info
    weight_loss_baking = models.DecimalField(_('Weight loss due to baking'), max_digits=4, decimal_places=2, default=0)
    salable_weight = models.DecimalField(_('Salable weight(usable)'), max_digits=5, decimal_places=2, default=0)

    # Computational ratios of yield test
    raw_usable_quantity_cost = models.PositiveIntegerField(_('Cost of raw usable quantity'), default=0)
    baked_usable_quantity_cost = models.PositiveIntegerField(_('Cost of baked usable quantity'), default=0)
    raw_usable_quantity_cost_per_press = models.PositiveIntegerField(_('Cost of raw usable quantity per press'), default=0)
    baked_usable_quantity_cost_per_press = models.PositiveIntegerField(_('Cost of baked usable quantity per press'), default=0)
    number_of_raw_use = models.PositiveIntegerField(_('Number of raw use'), default=0)
    number_of_baked_use = models.PositiveIntegerField(_('Number of baked use'), default=0)

    class Meta:
        verbose_name = _('Raw material')
        verbose_name_plural = _('Raw materials')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.raw_usable_quantity_cost:
            self.raw_usable_quantity_cost = self.price
        super().save(*args, **kwargs)

    def get_reduce_form_url(self):
        return reverse('restaurant:raw_materials_reduce_form', args=[self.pk])
