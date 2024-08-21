from django.utils.translation import gettext as _
from django.db.models import TextChoices


class ActivityFieldsTypeEnum(TextChoices):
    CATERING = 'catering', _('Catering')
    IRANIAN_RESTAURANT = 'iranian_restaurant', _('Iranian restaurant')
    NON_IRANIAN_RESTAURANT = 'non_iranian_restaurant', _('Non Iranian restaurant')
    COFFEE_SHOP = 'coffee_shop', _('Coffee Shop')
    CAFE_RESTAURANT = 'cafe_restaurant', _('Cafe Restaurant')
    OTHER = 'other', _('Other')


class WorkShiftsTypeEnum(TextChoices):
    MORNING = 'morning ', _('Morning')
    NOON = 'noon ', _('Noon')
    NIGHT = 'night ', _('Night')


class YesOrNoTypeEnum(TextChoices):
    YES = 'yes ', _('Yes')
    NO = 'no ', _('No')
