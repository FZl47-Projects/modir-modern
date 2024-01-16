from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.manager import Manager
from .utils import check_phone_number


# Custom Access manager
class AccessManager(Manager):
    def create_admin_access(self):
        obj, created = self.model.object.get_or_create(title=self.model.ACCESSES.ADMIN)

        return obj


# Custom User manager
class UserManager(BaseUserManager):
    def create_user(self, password=None, phone_number=None):
        """ Creates and saves a User with the given data. """

        if not check_phone_number(phone_number):
            raise ValidationError(_('Entered phone number is not valid'))

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password=None):
        """ Creates and saves a superuser with the given data. """

        if not phone_number:
            raise ValueError(_('Users must have a mobile number!'))

        user = self.create_user(password, phone_number)

        # Create admin access then add it to user accesses
        obj = user.accesses.create_admin_access()
        user.accesses.add(obj)

        user.is_admin = True  # Set as 'admin' user
        user.is_superuser = True
        user.is_verified = True

        user.save(using=self._db)

        return user
