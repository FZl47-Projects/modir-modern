from django.contrib import admin
from .models import Notification


# Register Notification admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_user', 'type', 'send_notify', 'created_at')
    list_display_links = ('id', 'to_user')
    list_filter = ('send_notify', 'is_showing', 'type')
    search_fields = ('to_user__phone_number',)
    readonly_fields = ('created_at', 'updated_at')
