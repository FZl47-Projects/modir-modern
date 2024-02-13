from django.utils.translation import gettext as _
from datetime import date, timedelta
from apps.subscription.models import Subscriber
from apps.notification.models import Notification


def notif_remain_days():
    """ Send notif(sms) to user if the subscription expire time is lesser than 4 days. """
    today = date.today()
    last_four_days = today + timedelta(days=4)

    subscribers = Subscriber.objects.filter(is_active=True, expire_date__lt=last_four_days)

    for obj in subscribers:
        Notification.objects.create(
            type=Notification.TYPES.SUBSCRIPTION_END_WARNING,
            title=_('Subscription end warning'),
            to_user=obj.user,
            kwargs={'days': (obj.expire_date - today).days}
        )


def deactivate_subs():
    """ Deactivate expired subscriptions everyday """
    today = date.today()

    expired_subs = Subscriber.objects.filter(is_active=True, expire_date__lt=today)
    expired_subs.update(is_active=False)
