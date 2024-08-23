from django.views.generic import ListView, FormView, DetailView, TemplateView
from django.shortcuts import reverse, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib import messages

from apps.restaurant.models import Restaurant, Recipe
from apps.account.forms import UpdateProfileForm
from apps.notification.models import Notification
from apps.notification.utils import create_notify_for_admins
from .models import CustomerSurvey
from . import forms, models


# Render Customer ServicesList view
class ServicesListView(DetailView):
    template_name = 'customers/services_list.html'
    model = Restaurant

    def get_object(self, queryset=None):
        obj = get_object_or_404(Restaurant, pk=self.request.GET.get('code'))
        return obj


# Render Customer DigitalMenu view
class DigitalMenuView(ListView):
    template_name = 'customers/digital_menu.html'
    model = Restaurant

    def filter(self, restaurant, objects):
        category = self.request.GET.get('category')
        if category:
            objects = objects.filter(category__title=category, is_material=False)
        else:
            objects = objects.filter(category=restaurant.recipes_categories.first(), is_material=False)

        return objects

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs.get('pk'))
        queryset = Recipe.objects.filter(category__restaurant=restaurant)

        queryset = self.filter(restaurant, queryset)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'restaurant': get_object_or_404(Restaurant, pk=self.kwargs.get('pk'))
        })

        return context


# Add CustomerSurveys view
class AddCustomerSurveysView(FormView):
    template_name = 'customers/services_list.html'
    form_class = forms.CustomerSurveyForm

    def get_success_url(self):
        restaurant = self.request.POST.get('restaurant')
        if restaurant:
            return reverse('customers:services_list') + f'?code={restaurant}'

        referer_url = self.request.META.get('HTTP_REFERER')
        return referer_url

    def form_valid(self, form):
        form.save()

        messages.success(self.request, _('Your rate has been successfully registered'))
        return super().form_valid(form)


# Render CustomersSurveysList view
class CustomerSurveysListView(ListView):
    template_name = 'customers/surveys_list.html'
    model = CustomerSurvey

    def get_queryset(self):
        queryset = CustomerSurvey.objects.filter(restaurant__user=self.request.user).reverse()
        return queryset


# Add Counseling view
class CounselingAddView(LoginRequiredMixin, TemplateView):
    template_name = 'customers/counseling/add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['Counseling'] = models.Counseling
        return context

    def get_redirect_url(self):
        referer_url = self.request.META.get('HTTP_REFERER')
        return referer_url

    def post(self, request):
        data = self.request.POST.copy()
        work_shifts = ' | '.join(data.getlist('work_shift', []))
        data['work_shift'] = work_shifts

        user = request.user
        if not user.is_profile_completed:
            form_user = UpdateProfileForm(data, instance=user.profile)
            if not form_user.is_valid():
                messages.error(self.request, _('Please enter fields correctly'))
                return redirect(self.get_redirect_url())
            form_user.save()

        form = forms.CounselingForm(data, files=self.request.FILES)
        if not form.is_valid():
            messages.error(self.request, _('Please enter fields correctly'))
            return redirect(self.get_redirect_url())
        obj = form.save()
        # create notification for user
        Notification.objects.create(
            type=Notification.TYPES.NEW_COUNSELING_FORM_SUBMITED,
            title=_('Your counseling form has been successfully submited'),
            to_user=obj.user,
            send_notify=True
        )
        # create notification for admin's
        create_notify_for_admins(
            Notification.TYPES.NEW_COUNSELING_FORM_SUBMITED_ADMIN,
            _('New counseling form submited')
        )
        messages.success(self.request, _('Your counseling form has been successfully submited'))
        return redirect(self.get_redirect_url())
