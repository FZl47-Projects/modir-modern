from django.views.generic import View, TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib import messages

from .models import Course


# Render CoursesList view
class CoursesListView(LoginRequiredMixin, ListView):
    template_name = 'course/list.html'
    model = Course

    def filter(self, objects):
        q = self.request.GET.get('type')
        if q:
            objects = objects.filter(type=q)
        return objects

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)

        return self.filter(queryset)
