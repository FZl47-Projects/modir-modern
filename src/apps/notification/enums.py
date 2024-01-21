from django.utils.translation import gettext as _
from django.db.models import TextChoices


# Notification Type choices
class NotificationTypes(TextChoices):
    MOBILE_VERIFICATION_CODE = 'MOBILE_VERIFICATION_CODE', _('Mobile verification code')
