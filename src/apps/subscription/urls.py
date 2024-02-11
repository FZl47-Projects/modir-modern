from django.urls import path
from . import views


app_name = 'subscription'

urlpatterns = [
    path('', views.SubscriptionListView.as_view(), name='subscription_list'),
    path('order/create/', views.CreateSubscriptionOrderView.as_view(), name='create_order'),
    path('add/', views.AddSubscriptionView.as_view(), name='add_subscription'),
]
