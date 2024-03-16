from django.urls import path
from . import views


app_name = 'customers'

urlpatterns = [
    path('', views.ServicesListView.as_view(), name='services_list'),
    path('<int:pk>/menu/', views.DigitalMenuView.as_view(), name='digital_menu'),
    path('survey/', views.AddCustomerSurveysView.as_view(), name='add_survey'),
    path('survey/list/', views.CustomerSurveysListView.as_view(), name='surveys_list'),
]
