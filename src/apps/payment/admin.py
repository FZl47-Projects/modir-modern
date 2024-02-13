from django.utils.translation import gettext as _
from django.contrib import admin

from .models import Order, OrderItem


# Register OrderItem as inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('object_id',)


# Register Order model admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('oid', 'user', 'get_place_name', 'payable_price', 'discount_price')
    list_display_links = ('oid', 'user')
    readonly_fields = ('payable_price', 'discount_price', 'bank_tracking_code')
    search_fields = ('oid', 'user__profile__place_name')
    inlines = [OrderItemInline]

    @admin.display(description=_('Place name'))
    def get_place_name(self, obj):
        return obj.user.profile.place_name

