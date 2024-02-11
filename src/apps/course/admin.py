from django.utils.translation import gettext as _
from django.contrib import admin
from django.db import models
from django import forms

from . models import Instructor, Course, Session, FAQ


# Register Instructors model admin
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

    fieldsets = (
        (None, {'fields': ('name', 'biography', 'image')}),
        (_('Media links'), {'fields': ('website', 'linkedin', 'instagram', 'twitter')})
    )


# Register Sessions as Inline
class SessionInline(admin.StackedInline):
    model = Session
    extra = 0


# Register FAQ as Inline
class FAQInline(admin.StackedInline):
    model = FAQ
    extra = 0

    # Change formfield attributes(widget:size)
    formfield_overrides = {models.CharField: {"widget": forms.TextInput(attrs={"size": "96"})}}


# Register Course model admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'instructor', 'type', 'discount', 'get_selling_price')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('is_active', 'type')
    readonly_fields = ('selling_price',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SessionInline, FAQInline]

    fieldsets = (
        (None, {'fields': ('title', 'slug', 'short_des', 'instructor', 'type', 'description')}),
        (_('Price info'), {'fields': ('payment_type', 'price', 'discount', 'selling_price')}),
        (_('Additional info'), {'fields': ('image', 'duration', 'pinned', 'is_active')})
    )

    # Change formfield attributes(widget:size)
    formfield_overrides = {models.CharField: {"widget": forms.TextInput(attrs={"size": "96"})}}

    @admin.display(description=_('Selling price(Rial)'))
    def get_selling_price(self, obj):
        return '{:,}'.format(obj.selling_price)
