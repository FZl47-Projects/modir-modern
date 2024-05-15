from django.utils.translation import gettext as _
from django.db.models import TextChoices


# SubscriptionTypes Enum
class SubscriptionTypesEnum(TextChoices):
    ONE_WEEK = (1 / 4), _('One week')
    ONE = 1, _('One month')
    TWO = 2, _('Two months')
    THREE = 3, _('Three months')
    SIX = 6, _('Six months')
    TWELVE = 12, _('Twelve months')
