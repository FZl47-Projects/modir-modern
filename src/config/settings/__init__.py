from .base import *
from os import getenv


PRODUCTION = getenv('PRODUCTION', False)

if PRODUCTION:
    from .production import *
else:
    from .development import *
