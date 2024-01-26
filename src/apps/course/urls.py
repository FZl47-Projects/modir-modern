from django.urls import path
from . import views


app_name = 'course'

urlpatterns = [
    path('list/', views.CoursesListView.as_view(), name='course_list'),
]
