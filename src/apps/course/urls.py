from django.urls import path, re_path
from . import views


app_name = 'course'

urlpatterns = [
    path('', views.CoursesListView.as_view(), name='course_list'),
    path('my-list/', views.UserCourseListView.as_view(), name='user_course_list'),
    path('purchase/', views.PurchaseCourseView.as_view(), name='purchase_course'),
    path('add/', views.AddCourseView.as_view(), name='add_course'),
    re_path(r'(?P<slug>[-\w]+)/', views.CourseDetailView.as_view(), name='course_detail'),
]
