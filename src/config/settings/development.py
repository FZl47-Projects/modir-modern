from .base import BASE_DIR
from os import getenv


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': getenv('SQLITE_PATH', BASE_DIR / 'db.sqlite3'),
    }
}


# Django-q config
Q_CLUSTER = {
    'name': 'django-q',
    'workers': int(getenv('Q_CLUSTER_WORKERS', 4)),
    'recycle': int(getenv('Q_CLUSTER_RECYCLE', 500)),
    'timeout': int(getenv('Q_CLUSTER_TIMEOUT', 60)),
    'compress': True,
    'queue_limit': 500,
    'orm': 'default',
}


# BankGateways settings
AZ_IRANIAN_BANK_GATEWAYS = {
   'GATEWAYS': {
       'IDPAY': {
           'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
           'METHOD': 'POST',  # GET or POST
           'SANDBOX': 1,  # 0 disable, 1 active
       },
   },
   'IS_SAMPLE_FORM_ENABLE': True,  # Optional(default is False)
   'DEFAULT': 'ZARINPAL',  # Required
   'CURRENCY': 'IRR',  # Optional
   'TRACKING_CODE_QUERY_PARAM': 'tc',  # Optional
   'TRACKING_CODE_LENGTH': 16,  # Optional
   'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader',  # Optional
   'BANK_PRIORITIES': ['IDPAY']
}
