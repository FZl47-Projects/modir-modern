from django import template

register = template.Library()


# Separate thousands filter
@register.filter
def intcomma(value):
    if value:
        return '{:,}'.format(value)
    return 0


@register.filter
# Convert rial filter
def convert_rial(value):
    if value:
        value = str(value)
        return int(value[:-1])
    return 0
