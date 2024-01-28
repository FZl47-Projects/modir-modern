from django.utils.translation import gettext as _
from django.db.models import TextChoices


# TicketTypes enum
class TicketTypesEnum(TextChoices):
    GENERAL = 'general', _('General problem')
    TECHNICAL = 'technical', _('Technical problem')


# TicketStatus enum
class TicketStatusEnum(TextChoices):
    OPEN = 'open', _('Open')
    CLOSE = 'close', _('Closed')
