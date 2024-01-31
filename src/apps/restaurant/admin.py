from django.contrib import admin
from . import models


# Register Restaurants admin
@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title')
    list_display_links = ('id', 'user')
    list_filter = ('is_active',)
    search_fields = ('user__phone_number',)


# Register RawMaterialCategories admin
@admin.register(models.RawMaterialCategory)
class RawMaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    list_display_links = ('id', 'title')
    list_filter = ('is_active',)
