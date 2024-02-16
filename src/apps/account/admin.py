from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
from django.contrib import admin

from .models import User, Access, UserProfile
from .forms import UserCreationForm


# Unregister the Group model from admin.
admin.site.unregister(Group)

# Register User Access model admin
admin.site.register(Access)


# User model admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The form to add user instances
    add_form = UserCreationForm

    list_display = ('id', '__str__', 'first_name', 'last_name', 'is_active', 'is_verified')
    list_display_links = ('id', '__str__',)
    readonly_fields = ('created_at', 'last_login',)
    list_filter = ('is_active', 'is_admin', 'is_verified', 'accesses',)
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
    date_hierarchy = 'created_at'


# Register UserProfile model admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'place_name', 'province')
    list_display_links = ('id', 'user')
    search_fields = ('user__phone_number', 'place_name')
    list_filter = ('gender',)
    autocomplete_fields = ('user',)
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {'fields': ('user',)}),
        (_('Personal info'), {'fields': ('melli_code', 'gender', 'date_of_birth')}),
        (_('Place info'), {'fields': ('place_name', 'province', 'city', 'image')}),
    )

    @admin.display(description=_('Place name'))
    def get_place_name(self, obj):
        return obj.user.profile.place_name
