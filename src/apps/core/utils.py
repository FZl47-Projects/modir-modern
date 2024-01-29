from django.utils.translation import gettext as _
from django.contrib.auth import settings
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

from threading import Thread
from os.path import splitext
from ippanel import Client


# Get time in format
def get_time(frmt: str = '%Y-%m-%d %H:%M'):
    now = timezone.now()
    if frmt is not None:
        now = now.strftime(frmt)

    return now


# Create image/file path based on time
def upload_file_src(instance, path):
    now = get_time('%Y-%m-%d')
    return f'files/{now}/{path}'


# Return file extension
def get_file_extension(file_name):
    name, extension = splitext(file_name.file.name)
    return extension


# Get coded phone number(IR)
def get_coded_phone_number(number):
    try:
        phone_number = str(number)
        return '+98' + phone_number[1:]
    except (TypeError, IndexError):
        return None


# Timesince in persian utils
def get_timesince_persian(time):
    time_server = timezone.now()

    diff_time = datetime(
        time_server.year, time_server.month, time_server.day, time_server.hour, time_server.minute
    ) - datetime(
        time.year, time.month, time.day, time.hour, time.minute
    )

    diff_time_sec = diff_time.total_seconds()

    minute = int(diff_time_sec // 60 % 60)
    hour = int(diff_time_sec // 3600)
    day = diff_time.days

    if minute > 0:
        output = _('%(minutes)s minutes ago.') % {'minutes': minute}
    elif hour > 0:
        output = _('%(hours)s hours ago.') % {'hours': hour}
    elif day > 0:
        output = _('%(days)s days ago.') % {'days': day}
    else:
        output = _('Moments ago')

    return output


# Form validator utils
def validate_form(request, form):
    if form.is_valid():
        return True

    errors = form.errors.items()

    if not errors:
        messages.error(request, _('Entered data is not correct.'))
        return False

    for field, message in errors:
        for error in message:
            messages.error(request, error)

    return False


# Toast form errors utils
def toast_form_errors(request, form):
    errors = form.errors.items()
    if not errors:
        messages.error(request, _('Entered data is not correct.'))
        return False

    for field, message in errors:
        for error in message:
            messages.error(request, error)


# Send SMS util
def send_sms(phone_number, pattern, **kwargs):
    phone_number = get_coded_phone_number(phone_number)
    phone_number = phone_number.replace('+', '')

    # Create client instance
    sms = Client(settings.SMS_CONFIG['API_KEY'])

    # Send sms via ippanel module
    t1 = Thread(target=sms.send_pattern, args=(
        pattern,  # pattern code
        settings.SMS_CONFIG['ORIGINATOR'],  # originator
        phone_number,  # recipient
        kwargs,  # pattern values
    ))
    t1.start()


# Remove first character from str
def remove_first_char(string):
    try:
        return string[1:] if string[0] == '0' else string
    except (TypeError, IndexError):
        return string
