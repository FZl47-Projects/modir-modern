from django.urls import path, re_path
from . import views


app_name = 'course'

urlpatterns = [
    path('', views.CoursesListView.as_view(), name='course_list'),
    path('my-list/', views.UserCourseListView.as_view(), name='user_course_list'),
    re_path(r'(?P<slug>[-\w]+)/', views.CourseDetailView.as_view(), name='course_detail'),
]
