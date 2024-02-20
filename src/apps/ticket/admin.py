from django.contrib import admin
from .models import Ticket, Messages


# Register TicketMessage model admin
@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    search_fields = ('user__phone_number',)

    def has_module_permission(self, request):
        return False


# Register Ticket Messages as Inline
class MessagesInline(admin.StackedInline):
    model = Messages
    extra = 0
    autocomplete_fields = ['user']


# Register Ticket model admin
@admin.register(Ticket)
class TicketModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'type', 'status')
    list_display_links = ('id', 'user', 'title')
    search_fields = ('user__phone_number', 'title')
    list_filter = ('type', 'status')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [MessagesInline]
