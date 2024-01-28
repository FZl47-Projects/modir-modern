from django.urls import path
from . import views


app_name = 'ticket'

urlpatterns = [
    path('', views.TicketListView.as_view(), name='ticket_list'),
    path('create/', views.TicketCreateView.as_view(), name='create_ticket'),
    path('<int:pk>/', views.TicketDetailsView.as_view(), name='ticket_details'),
    path('<int:pk>/message/', views.CreateMessageView.as_view(), name='ticket_create_message'),
]
