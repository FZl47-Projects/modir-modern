from django.utils.translation import gettext as _
from django.db import models

from apps.restaurant.models import Restaurant
from apps.core.models import BaseModel


# Customer's Survey model
class CustomerSurvey(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='customers_survey', verbose_name=_('Restaurant'))
    phone_number = models.CharField(_('Customer phone number'), max_length=16, null=True, blank=True)
    name = models.CharField(_('Customer name'), max_length=128, null=True, blank=True)
    comment = models.TextField(_('Customer comment'), null=True, blank=True)

    question1 = models.CharField(_('Answer of question 1'), max_length=64, null=True, blank=True)
    question2 = models.CharField(_('Answer of question 2'), max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = _('Customer survey')
        verbose_name_plural = _('Customers surveys')

    def __str__(self):
        return f'{self.restaurant.title} - {self.phone_number}'
