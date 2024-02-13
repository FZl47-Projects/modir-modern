from django.utils.translation import gettext as _
from django.db.models import TextChoices


# Notification Type choices
class NotificationTypes(TextChoices):
    MOBILE_VERIFICATION_CODE = 'MOBILE_VERIFICATION_CODE', _('Mobile verification code')
    SUBSCRIPTION_END_WARNING = 'SUBSCRIPTION_END_WARNING', _('Subscription end warning')
