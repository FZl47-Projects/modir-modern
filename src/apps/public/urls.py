from django.urls import path
from . import views


app_name = 'public'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('welcome', views.WelcomeView.as_view(), name='welcome'),
]
