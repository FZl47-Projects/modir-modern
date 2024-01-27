from django.urls import path
from . import views


app_name = 'subscription'

urlpatterns = [
    path('', views.SubscriptionListView.as_view(), name='subscription_list'),
]
