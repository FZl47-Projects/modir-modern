from django.contrib import admin
from .models import CustomerSurvey, Counseling


# Register CustomerSurveys admin
@admin.register(CustomerSurvey)
class CustomerSurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'restaurant', 'phone_number')
    list_display_links = ('id', 'name', 'restaurant')
    list_filter = ('question1', 'question2')
    search_fields = ('phone_number', 'restaurant__title')


@admin.register(Counseling)
class CounselingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__phone_number',)
