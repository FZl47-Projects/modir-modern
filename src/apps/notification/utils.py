from apps.account.models import User
from .models import Notification


def create_notify_for_admins(type, title):
    admins = User.objects.filter(is_admin=True)
    for admin in admins:
        Notification.objects.create(
            type=type,
            to_user=admin,
            title=title
        )
