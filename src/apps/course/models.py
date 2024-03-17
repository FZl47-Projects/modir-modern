from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.templatetags.static import static
from django.shortcuts import reverse
from django.db import models

from .utils import course_video_path, introduction_video_path, course_images_path
from .enums import CoursePaymentTypeEnum, CourseTypeEnum
from apps.core.models import BaseModel
from tinymce.models import HTMLField
from os.path import splitext
User = get_user_model()


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
    slug = models.SlugField(_('Slug'), max_length=255, null=True, blank=True, allow_unicode=True)
    short_des = models.CharField(_('Short description'), max_length=255, null=True, blank=True)
    description = HTMLField(verbose_name=_('Description'), default='')
    type = models.CharField(_('Course type'), max_length=32, choices=Types.choices, default=Types.OFFLINE)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, verbose_name=_('Instructor'), related_name='courses', null=True)
    duration = models.CharField(_('Duration'), max_length=128, help_text=_('2h, 30m'))
    payment_type = models.CharField(_('Payment type'), max_length=32, choices=PaymentTypes.choices, default=PaymentTypes.CASH)
    price = models.PositiveBigIntegerField(_('Price'), default=0)
    discount = models.IntegerField(_('Discount'), default=0)
    selling_price = models.PositiveBigIntegerField(_('Selling price'), default=0)

    introduction_video = models.FileField(_('Introduction video'), upload_to=introduction_video_path, null=True, blank=True)
    introduction_video_link = models.URLField(_('Introduction video'), null=True, blank=True)
    introduction_image = models.ImageField(_('Introduction image'), upload_to=course_images_path, null=True, blank=True)
    cover_image = models.ImageField(_('Image'), upload_to=course_images_path, null=True, blank=True)

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

    def get_type_label(self):
        return self.get_type_display()

    def get_absolute_url(self):
        return reverse('course:course_detail', args=[self.slug])

    def get_thumbnail_url(self):
        if self.introduction_image:
            return self.introduction_image.url

    def get_episode_count(self):
        return self.episodes.filter(is_active=True).count() or 0

    def get_sessions(self):
        return self.sessions.all()

    def get_faqs(self):
        return self.faqs.all()

    def get_comments(self):
        return self.comments.all()


# Course's sessions model
class Session(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions', verbose_name=_('Course'))
    title = models.CharField(_('Session title'), max_length=255, default=_('No title'))

    class Meta:
        verbose_name = _('Course session')
        verbose_name_plural = _('Course sessions')

    def __str__(self):
        return f'{self.course} - {self.title}'

    def get_episodes(self):
        return self.episodes.filter(is_active=True).order_by('number')


# Session's episodes model
class Episode(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='episodes', verbose_name=_('Course'))
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='episodes', verbose_name=_('Session'))
    title = models.CharField(_('Episode title'), max_length=255, default=_('No title'))
    number = models.PositiveSmallIntegerField(_('Episode number'))
    file = models.FileField(_('Video file'), upload_to=course_video_path, null=True, blank=True)
    file_url = models.URLField(_('File url'), null=True, blank=True)
    duration = models.PositiveSmallIntegerField(_('Duration'), default=0, null=True, blank=True, help_text=_('Minutes'))
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Episode')
        verbose_name_plural = _('Episodes')

    def __str__(self):
        return f'{self.session} - {self.title}'

    def get_file_url(self):
        if self.file:
            return self.file.url

    @property
    def is_video(self):
        name, extension = splitext(self.file_url)
        if extension in ['.mp4', 'm4v', '.mkv']:
            return True


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


# Course Comments model
class Comment(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Course'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='course_comments', verbose_name=_('User'), null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    text = models.TextField(max_length=512)
    is_verified = models.BooleanField(_('Verified'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Course comment')
        verbose_name_plural = _('Course comments')

    def __str__(self):
        return f'{self.user} - {self.course}'


# UserCourses model
class UserCourse(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name=_('User'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_courses', verbose_name=_('Course'))
    is_finished = models.BooleanField(_('Is finished'), default=False)

    class Meta:
        verbose_name = _('User course')
        verbose_name_plural = _('User courses')

    def __str__(self):
        return f'{self.user} - {self.course}'
