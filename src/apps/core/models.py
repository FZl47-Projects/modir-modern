from django.utils.translation import gettext as _
from django.db import models
from .utils import get_timesince_persian


class BaseModel(models.Model):
    created_at = models.DateTimeField(_('Creation time'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Update time'), auto_now=True)

    class Meta:
        abstract = True

    def get_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_created_date(self):
        return self.created_at.strftime('%Y-%m-%d')

    def get_created_at_time_past(self):
        return get_timesince_persian(self.created_at)
