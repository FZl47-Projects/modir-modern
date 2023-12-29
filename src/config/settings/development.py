from .base import BASE_DIR
from os import getenv


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / getenv('SQLITE_PATH', 'db.sqlite3'),
    }
}
