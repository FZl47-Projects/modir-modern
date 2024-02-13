from apps.core.utils import send_sms


class NotificationUser:

    @classmethod
    def mobile_verification_code_handler(cls, notification, phone_number):
        pattern = 'h63qzke49mrw4aq'
        send_sms(phone_number, pattern, code=notification.kwargs['code'])

    @classmethod
    def subscription_end_warning(cls, notification, phone_number):
        pattern = None  # TODO: Add pattern code from ippanel
        send_sms(phone_number, pattern, days=notification.kwargs['days'])


NOTIFICATION_USER_HANDLERS = {
    'MOBILE_VERIFICATION_CODE': NotificationUser.mobile_verification_code_handler,
    'SUBSCRIPTION_END_WARNING': NotificationUser.subscription_end_warning,
}
