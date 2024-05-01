from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re


# Get coded phone number(IR)
def get_coded_phone_number(number):
    phone_number = str(number)
    return '+98' + phone_number[1:]


# Get raw phone number(IR)
def get_raw_phone_number(number):
    phone_number = str(number)
    return '0' + phone_number[3:]


# Check phone number format(IR)
def check_phone_number(number):
    mobile_regex = "^09([0-9]{2}|[0-9]{3})-?[0-9]{3}-?[0-9]{4}$"
    if number and re.search(mobile_regex, number):
        return True

    return False


# Check email format
def check_email_format(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
