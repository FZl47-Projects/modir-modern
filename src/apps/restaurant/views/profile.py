from django.views.generic import TemplateView, FormView, DetailView, View
from django.shortcuts import redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages

from apps.subscription.mixinx import SubscriptionRequiredMixin
from apps.restaurant import models, forms


class Index(SubscriptionRequiredMixin, TemplateView):
    template_name = 'restaurant/profile/index.html'


class AddOrUpdateProfileView(SubscriptionRequiredMixin, View):

    def get_redirect_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request):
        data = request.POST.copy()
        user = request.user
        profile = user.get_profile()
        # additional values
        data['user'] = user

        f = forms.RestaurantProfileForm(data, instance=profile, files=request.FILES)
        if not f.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(self.get_redirect_url())
        f.save()
        messages.success(request, _('Operation completed successfully'))
        return redirect(self.get_redirect_url())


class AddFixedCostView(SubscriptionRequiredMixin, View):

    def get_redirect_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request):
        data = request.POST.copy()
        # additional values
        data['restaurant_profile'] = request.user.get_profile()
        f = forms.AddFixedCostForm(data, files=request.FILES)
        if not f.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(self.get_redirect_url())
        f.save()
        messages.success(request, _('Operation completed successfully'))
        return redirect(self.get_redirect_url())


class UpdateFixedCostProfileView(SubscriptionRequiredMixin, View):

    def get_redirect_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request, pk):
        data = request.POST.copy()
        obj = get_object_or_404(models.FixedCosts, id=pk, restaurant_profile__user=request.user)
        f = forms.UpdateFixedCostProfile(data, files=request.FILES, instance=obj)
        if not f.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(self.get_redirect_url())
        f.save()
        messages.success(request, _('Operation completed successfully'))
        return redirect(self.get_redirect_url())


class DeleteFixedCostView(SubscriptionRequiredMixin, View):

    def get_redirect_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request, pk):
        fixed_cost = get_object_or_404(models.FixedCosts, id=pk, restaurant_profile__user=request.user)
        fixed_cost.delete()
        messages.success(request, _('Operation completed successfully'))
        return redirect(self.get_redirect_url())


class AddOngoingCostView(SubscriptionRequiredMixin, View):

    def get_redirect_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request):
        data = request.POST.copy()
        # additional values
        data['restaurant_profile'] = request.user.get_profile()
        f = forms.AddOngoingCostForm(data, files=request.FILES)
        if not f.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(self.get_redirect_url())
        f.save()
        messages.success(request, _('Operation completed successfully'))
        return redirect(self.get_redirect_url())


class UpdateOngoingCostView(SubscriptionRequiredMixin, View):

    def get_redirect_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request, pk):
        data = request.POST.copy()
        obj = get_object_or_404(models.OngoingCosts, id=pk, restaurant_profile__user=request.user)
        f = forms.UpdateOngoingCostForm(data, files=request.FILES, instance=obj)
        if not f.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(self.get_redirect_url())
        f.save()
        messages.success(request, _('Operation completed successfully'))
        return redirect(self.get_redirect_url())


class DeleteOngoingCostView(SubscriptionRequiredMixin, View):

    def get_redirect_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request, pk):
        obj = get_object_or_404(models.OngoingCosts, id=pk, restaurant_profile__user=request.user)
        obj.delete()
        messages.success(request, _('Operation completed successfully'))
        return redirect(self.get_redirect_url())


class SalesEstimateView(SubscriptionRequiredMixin, TemplateView):
    template_name = 'restaurant/profile/sales_estimate.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('account:login')
        if not user.get_profile():
            return redirect('restaurant:profile_index')
        return super().dispatch(request, *args, **kwargs)


class AddIncomeProfileView(SubscriptionRequiredMixin, View):

    def get_redirect_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request):
        data = request.POST.copy()
        # additional values
        data['restaurant_profile'] = request.user.get_profile()
        f = forms.AddIncomeProfile(data, files=request.FILES)
        if not f.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(self.get_redirect_url())
        f.save()
        messages.success(request, _('Operation completed successfully'))
        return redirect(self.get_redirect_url())


class UpdateIncomeProfileView(SubscriptionRequiredMixin, View):

    def get_redirect_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request, pk):
        data = request.POST.copy()
        income = get_object_or_404(models.IncomeAndCostsProfile, id=pk, restaurant_profile__user=request.user)
        f = forms.UpdateIncomeProfile(data, files=request.FILES, instance=income)
        if not f.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(self.get_redirect_url())
        f.save()
        messages.success(request, _('Operation completed successfully'))
        return redirect(self.get_redirect_url())


class DeleteIncomeProfileView(SubscriptionRequiredMixin, View):

    def get_redirect_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request, pk):
        obj = get_object_or_404(models.IncomeAndCostsProfile, id=pk, restaurant_profile__user=request.user)
        obj.delete()
        messages.success(request, _('Operation completed successfully'))
        return redirect(self.get_redirect_url())
