from django.utils.translation import gettext as _
from django.db.models import TextChoices


# CourseType enums
class CourseTypeEnum(TextChoices):
    FREE = 'free', _('Free')
    CASH = 'cash', _('Cash')
