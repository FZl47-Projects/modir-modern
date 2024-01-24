from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class CourseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.course'
    verbose_name = _('Course')
