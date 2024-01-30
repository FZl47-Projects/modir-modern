from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class RestaurantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.restaurant'
    verbose_name = _('Restaurant')
