from django.contrib import admin
from . import models


# Register Restaurants admin
@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('user__phone_number',)


# Register RawMaterials as inline
class RawMaterialInline(admin.StackedInline):
    model = models.RawMaterial
    extra = 0


# Register RawMaterialCategories admin
@admin.register(models.RawMaterialCategory)
class RawMaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'title', 'created_at')
    list_display_links = ('id', 'restaurant', 'title')
    list_filter = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RawMaterialInline]
