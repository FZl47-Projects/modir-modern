from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='account:login'), name='logout'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/send-code/', views.SendCodeView.as_view(), name='send_code'),
    path('register/verify/', views.VerifyPhoneNumberView.as_view(), name='verify_phone'),

    path('password/reset/', views.GetPhoneNumberView.as_view(), name='get_phone_number'),
    path('password/reset/confirm/', views.ResetPassConfirmView.as_view(), name='reset_pass_confirm'),
    path('password/reset/complete/', views.ResetPassCompleteView.as_view(), name='reset_pass_complete'),
]
