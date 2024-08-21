from django.utils.translation import gettext as _
from django.db import models

from apps.restaurant.models import Restaurant
from apps.core.models import BaseModel
from apps.customers import enums


# Customer's Survey model
class CustomerSurvey(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='customers_survey',
                                   verbose_name=_('Restaurant'))
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


class Counseling(models.Model):
    FIELDS = enums.ActivityFieldsTypeEnum
    WORK_SHIFTS = enums.WorkShiftsTypeEnum
    CONTROL_COST_SYSTEM = enums.YesOrNoTypeEnum
    BOOK_OF_REGULATIONS = enums.YesOrNoTypeEnum
    TASKS_WRITTEN = enums.YesOrNoTypeEnum
    RECIPES_WRITTEN = enums.YesOrNoTypeEnum
    INSTRUCTION_WRITTEN = enums.YesOrNoTypeEnum

    user = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name=_('User'))
    field_of_activity = models.CharField(max_length=25, choices=FIELDS.choices, verbose_name=_('Field of Activity'))
    work_experience = models.CharField(max_length=20, verbose_name=_('Work Experience'))
    work_shift = models.CharField(max_length=50, verbose_name=_('Work Shift'), null=True, blank=True)
    number_of_staff = models.IntegerField(_('Number of staff'))
    capacity = models.IntegerField(_('Capacity'))
    personnel_training = models.TextField(null=True, blank=True, verbose_name=_('Personnel Training Detail'))
    business_concerns = models.TextField(null=True, blank=True, verbose_name=_('Business Concerns Detail'))
    accounting_software = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Accounting Software'))
    conduct_inventory_reconciliation = models.CharField(max_length=100, null=True, blank=True,
                                                        verbose_name=_('Conduct Inventory Reconciliation'))

    has_control_cost_system = models.CharField(max_length=5, choices=CONTROL_COST_SYSTEM.choices,
                                               verbose_name=_('Has Control Cost System'), null=True, blank=True)

    has_book_of_regulations = models.CharField(max_length=5, choices=BOOK_OF_REGULATIONS.choices,
                                               verbose_name=_('Has Book of Regulations'), null=True, blank=True)

    has_tasks_written = models.CharField(max_length=5, choices=TASKS_WRITTEN.choices,
                                         verbose_name=_('Has Tasks Written'), null=True, blank=True)

    has_recipes_written = models.CharField(max_length=5, choices=RECIPES_WRITTEN.choices,
                                           verbose_name=_('Has Recipes Written'), null=True, blank=True)

    has_instructions_written = models.CharField(max_length=5, choices=INSTRUCTION_WRITTEN.choices,
                                                verbose_name=_('Has Instructions Written'), null=True, blank=True)

    class Meta:
        verbose_name = _('Counseling')
        verbose_name_plural = _('Counselings')
