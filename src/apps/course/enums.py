from django.utils.translation import gettext as _
from django.db.models import TextChoices


# CoursePaymentType enum
class CoursePaymentTypeEnum(TextChoices):
    FREE = 'free', _('Free')
    CASH = 'cash', _('Cash')


# CourseType enum
class CourseTypeEnum(TextChoices):
    IN_PERSON = 'in_person', _('In person')
    ONLINE = 'online', _('Online')
    OFFLINE = 'offline', _('Offline')
