from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _
from django.templatetags.static import static
from django.shortcuts import reverse
from django.db import models

from .enums import UserAccessEnum, UserGenderEnum
from .managers import UserManager, AccessManager
from .validators import validate_didit_type
from apps.core.models import BaseModel
from datetime import datetime
from secrets import token_hex


# Accesses model
class Access(models.Model):
    ACCESSES = UserAccessEnum

    title = models.CharField(_('Access title'), max_length=32, choices=ACCESSES.choices, default=ACCESSES.USER, unique=True)
    created_at = models.DateTimeField(_('Creation time'), auto_now_add=True)

    object = AccessManager()

    class Meta:
        verbose_name = _('Access')
        verbose_name_plural = _('Accesses')

    def __str__(self):
        return self.title

    def get_title_label(self):
        return self.get_title_display()


# Custom User model
class User(AbstractBaseUser, PermissionsMixin):
    ACCESSES = UserAccessEnum

    # Fields
    phone_number = models.CharField(_('Phone number'), max_length=11, unique=True)
    email = models.EmailField(_("Email address"), max_length=255, null=True, blank=True)
    first_name = models.CharField(_('First name'), max_length=128, null=True, blank=True)
    last_name = models.CharField(_('Last name'), max_length=128, null=True, blank=True)
    accesses = models.ManyToManyField(verbose_name=_('Accesses'), to=Access, related_name='user', blank=True)
    is_active = models.BooleanField(_("Active"), default=True)
    is_admin = models.BooleanField(_("Admin"), default=False)
    is_verified = models.BooleanField(_('Verify'), default=False)

    # Secret token
    token = models.CharField(_("Secret token"), max_length=64, null=True, blank=True, editable=False)

    created_at = models.DateTimeField(_('Creation time'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Update time'), auto_now=True)

    objects = UserManager()  # Set UserManager as model object manager

    USERNAME_FIELD = "phone_number"

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.phone_number

    @property
    def is_staff(self):
        """ Is the user a member of staff? """
        return self.is_admin

    @property
    def has_admin_access(self):
        """ Does the user have admin access? """
        if self.accesses.filter(title=self.ACCESSES.ADMIN).exists():
            return True
        return False

    def has_specific_access(self, access=None):
        """ Does the user have a specific access? """
        if self.accesses.filter(title=access).exists():
            return True
        return False

    def get_full_name(self):
        """ Return the user full name (first_name + last_name) """
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        return _('No name')

    def generate_token(self, byte: int = 12):
        self.token = token_hex(byte)
        self.save()

        return self.token

    def clear_token(self, request):
        if 'secret_token' in request.session:
            del request.session['secret_token']

        self.token = None
        self.save()

    def get_subscription_time(self):
        subscriptions = self.subscriptions.filter(is_active=True)
        remaining_days = sum([(sub.expire_date - datetime.now().date()).days for sub in subscriptions])

        return remaining_days

    def get_tickets_count(self):
        return self.tickets.all().count() or 0


# UserProfiles model
class UserProfile(BaseModel):
    GENDERS = UserGenderEnum

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))
    melli_code = models.CharField(_('Melli code'), max_length=10, validators=[validate_didit_type], null=True, blank=True)
    gender = models.CharField(_('Gender'), max_length=8, choices=GENDERS.choices, null=True, blank=True)
    date_of_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    place_name = models.CharField(_('Place name'), max_length=128, null=True, blank=True)
    province = models.CharField(_('Province'), max_length=64, null=True, blank=True)
    city = models.CharField(_('City'), max_length=64, null=True, blank=True)
    image = models.ImageField(_('Picture'), upload_to='images/profiles/', null=True, blank=True)

    class Meta:
        verbose_name = _('User profile')
        verbose_name_plural = _('Users profile')

    def __str__(self):
        return f'{self.user}'

    def get_absolute_url(self):
        return reverse('account:profile_details', self.pk)

    def get_gender_label(self):
        return self.get_gender_display()

    def get_image_url(self):
        if self.image:
            return self.image.url
        return static('images/defaults/user-profile-3.webp')
