from django.urls import path
from . import views


app_name = 'payment'

urlpatterns = [
    path('create-bank/', views.CreateBankGatewayView.as_view(), name='create_bank'),
    path('success/', views.CallBackSuccessView.as_view(), name='callback_success'),
    path('failed/', views.CallBackFailedView.as_view(), name='callback_failed'),
]
