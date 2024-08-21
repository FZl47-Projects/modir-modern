from apps.core.utils import send_sms


class NotificationUser:

    @classmethod
    def mobile_verification_code_handler(cls, notification, phone_number):
        pattern = 'h63qzke49mrw4aq'
        send_sms(phone_number, pattern, code=notification.kwargs['code'])

    @classmethod
    def subscription_end_warning(cls, notification, phone_number):
        pattern = '4qkv8ckgt5332k6'
        send_sms(phone_number, pattern, days=notification.kwargs['days'])

    @classmethod
    def new_ticket_created(cls, notification, phone_number):
        pattern = '1tqgkyl63l31fr6'
        send_sms(phone_number, pattern, user_name=notification.to_user.get_full_name())

    @classmethod
    def new_ticket_created_admin(cls, notification, phone_number):
        pattern = 'r1ls00hm3euo09o'
        send_sms(phone_number, pattern, user_name=notification.to_user.get_full_name())

    @classmethod
    def new_subscription_registered_admin(cls, notification, phone_number):
        pattern = 'mkomyeb4pc763kk'
        send_sms(phone_number, pattern, user_name=notification.to_user.get_full_name())

    @classmethod
    def new_subscription_registered(cls, notification, phone_number):
        pattern = '-'
        send_sms(phone_number, pattern, user_name=notification.to_user.get_full_name())

    @classmethod
    def new_user_registered_admin(cls, notification, phone_number):
        pattern = '-'
        send_sms(phone_number, pattern, user_name=notification.to_user.get_full_name())


NOTIFICATION_USER_HANDLERS = {
    'MOBILE_VERIFICATION_CODE': NotificationUser.mobile_verification_code_handler,
    'NEW_SUBSCRIPTION_REGISTERED_ADMIN': NotificationUser.new_subscription_registered_admin,
    'NEW_USER_ADMIN': NotificationUser.new_user_registered_admin,  # TODO: add pattern new sms type
    'NEW_COUNSELING_FORM_SUBMITED': NotificationUser.new_subscription_registered,  # TODO: add pattern new sms type
    'SUBSCRIPTION_END_WARNING': NotificationUser.subscription_end_warning,
    'NEW_TICKET_CREATED': NotificationUser.new_ticket_created,
    'NEW_TICKET_CREATED_ADMIN': NotificationUser.new_ticket_created_admin,
}
