from django.utils.translation import gettext as _
from django.contrib import admin
from django.db import models
from django import forms

from .models import Subscription, Subscriber


# Register Subscription model admin
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'discount', 'get_selling_price')
    list_display_links = ('id', 'type')
    list_filter = ('is_active',)
    readonly_fields = ('selling_price',)

    fieldsets = (
        (None, {'fields': ('type',)}),
        (_('Price info'), {'fields': ('price', 'discount', 'selling_price')}),
        (_('Status info'), {'fields': ('promo', 'is_active')})
    )

    formfield_overrides = {models.PositiveIntegerField: {"widget": forms.NumberInput(attrs={"size": "30"})}}

    @admin.display(description=_('Selling price(Rial)'))
    def get_selling_price(self, obj):
        return '{:,}'.format(obj.selling_price)


# Register Subscribers model admin
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_place_name', 'get_expire_date', 'is_active')
    list_display_links = ('id', 'user')
    readonly_fields = ('created_at',)
    list_filter = ('is_active',)
    search_fields = ('user__phone_number', 'user__profile__place_name')

    @admin.display(description=_('Expire date'))
    def get_expire_date(self, obj):
        return obj.expire_date.strftime('%Y-%m-%d')

    @admin.display(description=_('Place name'))
    def get_place_name(self, obj):
        return obj.user.profile.place_name
