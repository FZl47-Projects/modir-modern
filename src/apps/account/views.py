from django.shortcuts import redirect, reverse, get_object_or_404
from django.views.generic import View, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages


from apps.core.utils import toast_form_errors
from .mixinx import LogoutRequiredMixin
from .models import User, UserProfile
from . import forms
from random import randint


# Render Login view
class LoginView(LogoutRequiredMixin, FormView):
    template_name = 'account/login.html'
    form_class = forms.LoginForm
    success_url = '/'

    def remember_me(self, form):
        remember_me = form.cleaned_data.get('remember_me', False)
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

    def form_valid(self, form):
        user = form.cleaned_data.get('user')

        # Redirect to phone verification if user is not verified
        if not user.is_verified:
            token = user.generate_token()
            self.request.session['register_token'] = token

            return redirect('account:send_code')

        # Login user and set session expiry time
        login(self.request, user=user)
        self.remember_me(form)

        messages.success(self.request, _('Login successful'))
        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


# Render Register view
class RegisterView(LogoutRequiredMixin, FormView):
    template_name = 'account/register.html'
    form_class = forms.UserCreationForm
    success_url = reverse_lazy('account:send_code')

    def form_valid(self, form):
        user = form.save()

        # Create register token and save it in sessions
        token = user.generate_token()
        self.request.session['register_token'] = token
        
        return super().form_valid(form)
        
    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


# SendCode view
class SendCodeView(LogoutRequiredMixin, View):
    def get_redirect_url(self):
        next_url = self.request.GET.get('next', reverse('account:verify_phone'))
        return next_url

    def get(self, request):
        code = randint(10000, 99999)
        request.session['verify_code'] = code

        token = request.session.get('register_token')
        try:
            User.objects.get(token=token)
        except User.DoesNotExist:
            messages.error(request, _('There is an issue! please try again'))
            return redirect('account:register')

        # TODO: Send notification

        print(code)
        messages.info(request, _('Code sent to you'))
        return redirect(self.get_redirect_url())


# Render VerifyPhoneNumber view
class VerifyPhoneNumberView(LogoutRequiredMixin, FormView):
    template_name = 'account/verify_phone.html'
    form_class = forms.VerifyPhoneNumberForm
    success_url = '/'

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        data['data'] = {
            'code': self.request.POST.get('code'),
            'verify_code': self.request.session.get('verify_code'),
            'token': self.request.session.get('register_token')
        }

        return data

    def form_valid(self, form):
        user = form.cleaned_data.get('user')

        # Verify user and clear token
        user.is_verified = True
        user.clear_token(self.request)
        login(self.request, user)

        # Delete code from session
        if 'verify_code' in self.request.session:
            del self.request.session['verify_code']

        messages.success(self.request, _('Register done successful'))
        return redirect('/')
    
    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)
