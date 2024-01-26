from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.shortcuts import redirect, reverse

from apps.course.models import Course


# Render Index view
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'public/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'courses': Course.objects.filter(is_active=True).order_by('-id')[:5]
        })

        return context
