from django.utils.translation import gettext as _
from django.db.models import TextChoices


# UserAccess Enums
class UserAccessEnum(TextChoices):
    USER = 'user', _('User')
    ADMIN = 'admin', _('Admin')


# UserGender Enums
class UserGenderEnum(TextChoices):
    MALE = 'm', _('Male')
    FEMALE = 'f', _('Female')
