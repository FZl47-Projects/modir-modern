from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('register/send-code/', views.SendCodeView.as_view(), name='send_code'),
    path('register/verify/', views.VerifyPhoneNumberView.as_view(), name='verify_phone'),
]
