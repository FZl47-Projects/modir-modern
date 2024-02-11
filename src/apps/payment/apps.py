from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.payment'
    verbose_name = _('Payment')

    def ready(self):
        from . import signals
