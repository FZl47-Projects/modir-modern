from django.contrib import admin
from .models import TopBanner, IndexVideo


# Register TopBanners admin
@admin.register(TopBanner)
class TopBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'link', 'image')
    list_display_links = ('id', 'title', 'link')
    list_filter = ('is_active',)


# Register IndexVideo admin
@admin.register(IndexVideo)
class IndexVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active')
    list_display_links = ('id', 'title')
    list_filter = ('is_active',)
    fields = ('title', 'video', 'description', 'is_active')
