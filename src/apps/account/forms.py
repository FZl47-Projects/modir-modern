from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from django import forms

from .utils import check_phone_number
from .models import User, UserProfile
from persian_tools import digits


# Custom User creation form
class UserCreationForm(forms.ModelForm):
    """ A form for creating new users. Includes all the required
    fields, plus a repeated password. """

    phone_number = forms.CharField(label=_('Phone number'), max_length=11)
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password repeat'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number',)

    def clean_phone_number(self):
        # Check phone number format
        phone_number = self.cleaned_data.get('phone_number')
        phone_number = digits.convert_to_en(phone_number)

        if not check_phone_number(phone_number):
            raise ValidationError(_('Enter a valid phone number'))

        return phone_number

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Passwords are not match.'))

        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()

        return user


# Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=11, required=True, widget=forms.TextInput(attrs={'placeholder': _('09__')}))
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        username = digits.convert_to_en(username)

        # Check username format (username is phone number here)
        if not check_phone_number(username):
            raise ValidationError(_('Enter a valid phone number'), code='BAD-USERNAME')

        # Authenticate user and return it
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError(_('Username or password is not correct'), code='USER-NOT-FOUND')

        return {'user': user, 'remember_me': self.cleaned_data.get('remember_me')}


# VerifyPhoneNumber form
class VerifyPhoneNumberForm(forms.Form):
    code = forms.CharField(max_length=5, required=True, widget=forms.NumberInput)
    verify_code = forms.CharField(max_length=5, required=False, widget=forms.NumberInput)
    token = forms.CharField(max_length=32, required=False, widget=forms.TextInput)

    def clean(self):
        try:
            user = User.objects.get(token=self.cleaned_data['token'])
        except (User.DoesNotExist, TypeError, KeyError):
            raise ValidationError(_('There is an issue! please try again'), code='USER-NOT-FOUND')

        if self.cleaned_data['code'] != self.cleaned_data['verify_code']:
            raise ValidationError(_('Entered code is not correct'), code='WRONG-DATA')

        return {'user': user}


# GetPhoneNumber form
class GetPhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'placeholder': '09__'}))

    def clean(self):
        try:
            if not check_phone_number(self.cleaned_data['phone_number']):
                raise ValidationError(_('Enter a valid phone number'), code='BAD-PHONE-NUMBER')

            user = User.objects.get(phone_number=self.cleaned_data['phone_number'])
        except (User.DoesNotExist, TypeError, KeyError):
            raise ValidationError(_('No user found with this phone number'))

        return {'user': user}


# ResetPass form
class ResetPassForm(forms.Form):
    password = forms.CharField(max_length=128, min_length=4, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=128, min_length=4, required=True, widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Passwords are not match.'))

        return password2


# UpdateProfile form
class UpdateProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=11, required=True, widget=forms.TextInput)

    class Meta:
        model = UserProfile
        fields = ('city', 'province', 'place_name', 'image')

    def save(self, commit=True):
        profile = super().save()
        user = profile.user

        user.phone_number = self.cleaned_data.get('phone_number')
        if commit:
            user.save()

        return profile
