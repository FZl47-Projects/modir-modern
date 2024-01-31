from django.utils.translation import gettext as _
from django.templatetags.static import static
from django.shortcuts import reverse
from django.db import models

from .enums import CoursePaymentTypeEnum, CourseTypeEnum
from apps.core.models import BaseModel


# Instructors model
class Instructor(BaseModel):
    name = models.CharField(_('Instructor name'), max_length=128, default=_('No name'))
    biography = models.TextField(_('Biography'), null=True, blank=True)
    image = models.ImageField(_('Profile pic'), upload_to='images/instructors/')

    # Media pages
    linkedin = models.URLField(_('Linkedin url'), null=True, blank=True)
    instagram = models.URLField(_('Instagram url'), null=True, blank=True)
    twitter = models.URLField(_('X/Twitter url'), null=True, blank=True)
    website = models.URLField(_('Website url'), null=True, blank=True)

    class Meta:
        verbose_name = _('Instructor')
        verbose_name_plural = _('Instructors')

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image:
            return self.image.url

    def get_courses(self):
        return self.courses.all()

    def get_courses_count(self):
        return self.courses.all().count() or 0


# Courses model
class Course(BaseModel):
    Types = CourseTypeEnum
    PaymentTypes = CoursePaymentTypeEnum

    title = models.CharField(_('Title'), max_length=128, default=_('No title'))
    short_des = models.CharField(_('Short description'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    type = models.CharField(_('Course type'), max_length=32, choices=Types.choices, default=Types.OFFLINE)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, verbose_name=_('Instructor'), related_name='courses', null=True)
    duration = models.CharField(_('Duration'), max_length=255, help_text=_('2h, 30m'))
    payment_type = models.CharField(_('Payment type'), max_length=32, choices=PaymentTypes.choices, default=PaymentTypes.CASH)
    price = models.PositiveBigIntegerField(_('Price'), default=0)
    discount = models.IntegerField(_('Discount'), default=0)
    selling_price = models.PositiveBigIntegerField(_('Selling price'), default=0)
    image = models.ImageField(_('Image'), upload_to='images/courses/', null=True, blank=True)

    pinned = models.BooleanField(_('Pinned'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.selling_price = int(self.price - (self.price * (self.discount / 100)))
        super().save(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return static('images/logo-yellow.png')

    def get_type_label(self):
        return self.get_type_display()

    def get_absolute_url(self):
        return reverse('course:course_list')  # TODO: Add specific url

    def get_sessions(self):
        self.sessions.filter(is_active=True)

    def get_sessions_count(self):
        return self.sessions.all().count() or 0


# Course's sessions model
class Session(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions', verbose_name=_('Course'))
    title = models.CharField(_('Session title'), max_length=255, default=_('No title'))
    file = models.FileField(_('Video file'), upload_to='files/video/courses/')
    duration = models.PositiveIntegerField(_('Duration'), default=0, help_text=_('Seconds'))
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Course session')
        verbose_name_plural = _('Course sessions')
        ordering = ('-id',)

    def __str__(self):
        return self.course

    def get_file_url(self):
        if self.file:
            return self.file.url


# Courses FAQs
class FAQ(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='faqs', verbose_name=_('Course'))
    question = models.CharField(_('Question title'), max_length=255)
    answer = models.TextField(_('Answer'))

    class Meta:
        verbose_name = _('Frequently asked question')
        verbose_name_plural = _('Frequently asked questions')

    def __str__(self):
        return f'{self.course} - {self.question}'
