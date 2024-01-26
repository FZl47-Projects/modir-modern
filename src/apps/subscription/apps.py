from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class SubscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.subscription'
    verbose_name = _('Subscription')
