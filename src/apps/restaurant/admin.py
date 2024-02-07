from django.utils.translation import gettext as _
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


# Register RawMaterialCategories admin
@admin.register(models.RawMaterialCategory)
class RawMaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'title', 'created_at')
    list_display_links = ('id', 'restaurant', 'title')
    list_filter = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')


# Register RawMaterial model admin
@admin.register(models.RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'use_for')
    list_display_links = ('id', 'category', 'title')

    fieldsets = (
        (None, {'fields': ('category', 'title', 'use_for', 'price',)}),
        (_('Common info'), {'fields': ('quantity_raw_press', 'quantity_baked_press', 'delivery_weight')}),
        (_('Weight loss during cleaning'), {'fields': ('weight_loss_cleaning_usable', 'weight_loss_cleaning_unusable', 'edible_cleaned_weight')}),
        (_('Weight loss during baking'), {'fields': ('weight_loss_baking', 'salable_weight')}),
        (_('Computational ratios of yield'), {'fields': (
            'raw_usable_quantity_cost', 'baked_usable_quantity_cost', 'raw_usable_quantity_cost_per_press', 'baked_usable_quantity_cost_per_press',
            'number_of_raw_use', 'number_of_baked_use',
        )}),
    )


# ------------------------------------------


# Register RecipeCategory model admin
admin.site.register(models.RecipesCategory)


# Register Recipe model admin
admin.site.register(models.Recipe)

# Register RecipeCategory model admin
admin.site.register(models.RecipeMaterial)
