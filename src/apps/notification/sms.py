from apps.core.utils import send_sms


class NotificationUser:

    @classmethod
    def mobile_verification_code_handler(cls, notification, phone_number):
        pattern = 'h63qzke49mrw4aq'
        send_sms(phone_number, pattern, code=notification.kwargs['code'])

    # TODO: Add more sms handlers for other notifications


NOTIFICATION_USER_HANDLERS = {
    'MOBILE_VERIFICATION_CODE': NotificationUser.mobile_verification_code_handler,
}
