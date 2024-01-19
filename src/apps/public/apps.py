from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class PublicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.public'
    verbose_name = _('Public')
