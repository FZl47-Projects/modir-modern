from .base import REDIS_CONFIG
from os import getenv


# Database (postgresql)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": getenv("DB_NAME"),
        "USER": getenv("DB_USER"),
        "PASSWORD": getenv("DB_PASSWORD"),
        "HOST": getenv("DB_HOST"),
        "PORT": getenv("DB_PORT"),
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
    'redis': {
        'host': REDIS_CONFIG['host'],
        'port': REDIS_CONFIG['port'],
        'db': 0,
    }
}


# BankGateways config
AZ_IRANIAN_BANK_GATEWAYS = {
   'GATEWAYS': {
       'ZARINPAL': {
           'MERCHANT_CODE': getenv('ZARINPAL_MERCHANT_CODE'),
           'SANDBOX': 0,  # 0 disable, 1 active
       },
   },
   'IS_SAMPLE_FORM_ENABLE': False,  # Optional(default is False)
   'DEFAULT': 'ZARINPAL',  # Required
   'CURRENCY': 'IRR',  # Optional
   'TRACKING_CODE_QUERY_PARAM': 'tc',  # Optional
   'TRACKING_CODE_LENGTH': 16,  # Optional
   'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader',  # Optional
   'IS_SAFE_GET_GATEWAY_PAYMENT': True,
}
