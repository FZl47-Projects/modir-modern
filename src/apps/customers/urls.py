from django.urls import path
from . import views


app_name = 'customers'

urlpatterns = [
    path('', views.ServicesListView.as_view(), name='services_list'),
    path('<int:pk>/menu/', views.DigitalMenuView.as_view(), name='digital_menu'),
]
