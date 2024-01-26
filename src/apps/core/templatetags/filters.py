from django.utils.translation import gettext as _
from django import template

register = template.Library()


# Convert rial filter
@register.filter
def convert_rial(value):
    if value:
        value = str(value)
        return int(value[:-1])
    return 0


# Separate thousands filter
@register.filter
def intcomma(value):
    if value:
        return '{:,}'.format(value)
    return 0
