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


# Return Suggested price
@register.filter
def suggested_price(value):
    if value:
        return int(value * 1.5)


# Return Sales share percentage
@register.filter
def sales_percentage(obj, total):
    if total:
        return (obj.number_sold / total) * 100
