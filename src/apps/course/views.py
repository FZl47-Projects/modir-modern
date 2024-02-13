from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Course, UserCourse


# Render CoursesList view
class CoursesListView(LoginRequiredMixin, ListView):
    template_name = 'course/list.html'
    model = Course

    def filter(self, objects):
        q = self.request.GET.get('type')
        if q:
            objects = objects.filter(payment_type=q)
        return objects

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)
        return self.filter(queryset)


# Render CourseDetail view
class CourseDetailView(LoginRequiredMixin, DetailView):
    template_name = 'course/details.html'
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_course'] = UserCourse.objects.filter(course=self.object, user=self.request.user).exists()

        return context


# Render UserCourseList view
class UserCourseListView(LoginRequiredMixin, ListView):
    template_name = 'course/user_list.html'
    model = Course

    def get_queryset(self):
        queryset = Course.objects.filter(user_courses__user=self.request.user)
        return queryset
