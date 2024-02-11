from django.db import IntegrityError, InternalError
from .models import Order, OrderItem

ORDER_SESSION_KEY = "order"
