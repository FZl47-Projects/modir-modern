from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
from django.db import models as a_model
from django.contrib import admin
from django import forms

from .forms import UserCreationForm
from .models import User, Access


# Unregister the Group model from admin.
admin.site.unregister(Group)

# Register User Access model admin
admin.site.register(Access)


# User model admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The form to add user instances
    add_form = UserCreationForm

    list_display = ('id', '__str__', 'email', 'first_name', 'last_name', 'is_active', 'is_verified')
    list_display_links = ('id', '__str__', 'email',)
    readonly_fields = ('created_at', 'last_login',)
    list_filter = ('is_active', 'accesses',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password',)}),
        (_('Personal info'), {'fields': ('email', 'first_name', 'last_name',)}),
        (_('Verifications'), {'fields': ('is_active', 'is_verified', 'is_admin', 'is_superuser')}),
        (_('Permissions'), {'fields': ('user_permissions',)}),
        (_('Accesses'), {'fields': ('accesses',)}),
        (_('Dates'), {'fields': ('last_login', 'created_at',)}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'password1', 'password2'),
        }),
    )

    # Add search and ordering fields
    search_fields = ('phone_number', 'last_name')
    ordering = ('phone_number',)
    filter_horizontal = ('accesses', 'user_permissions')
