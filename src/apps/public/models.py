from django.utils.translation import gettext as _
from django.db import models

from apps.core.models import BaseModel


# TopBanners model
class TopBanner(BaseModel):
    title = models.CharField(_('Title'), max_length=128, null=True, blank=True)
    link = models.URLField(_('Related link'), null=True, blank=True)
    image = models.ImageField(_('Image'), upload_to='images/banners/')
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.id} - {self.link}'

    def get_image_url(self):
        if self.image:
            return self.image.url


# IndexVideo model
class IndexVideo(BaseModel):
    title = models.CharField(_('Title'), max_length=255, default=_('No title'))
    description = models.TextField(_('Description'), max_length=512, null=True, blank=True)
    cover = models.ImageField(_('Video cover'), upload_to='images/index/', null=True, blank=True)
    video = models.FileField(_('Video'), upload_to='images/index/', null=True, blank=True)
    video_url = models.URLField(_('Video url'), default='')
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Index video')
        verbose_name_plural = _('Index Videos')

    def __str__(self):
        return f'{self.title}'

    def get_cover_url(self):
        if self.cover:
            return self.cover.url
