from django.views.generic import View, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import Subscription


# Render SubscriptionList view
class SubscriptionListView(LoginRequiredMixin, ListView):
    template_name = 'subscription/list.html'
    model = Subscription
    queryset = Subscription.objects.filter(is_active=True)
