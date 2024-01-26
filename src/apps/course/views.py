from django.views.generic import View, TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.shortcuts import redirect, reverse
from django.contrib import messages

from .models import Course


# Render CoursesList view
class CoursesListView(LoginRequiredMixin, ListView):
    template_name = 'course/list.html'
    model = Course
    queryset = Course.objects.filter(is_active=True)
