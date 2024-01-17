from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_didit_type(value):
    if not value.isdigit():
        raise ValidationError(_('Entered value must be number'))

    return value
