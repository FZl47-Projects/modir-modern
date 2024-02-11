from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

from azbankgateways.urls import az_bank_gateways_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('froala-editor/', include('froala_editor.urls')),
    path('bankgateways/', az_bank_gateways_urls()),
    path('account/', include('apps.account.urls', namespace='account')),
    path('', include('apps.public.urls', namespace='public')),
    path('course/', include('apps.course.urls', namespace='course')),
    path('ticketing/', include('apps.ticket.urls', namespace='ticket')),
    path('subscription/', include('apps.subscription.urls', namespace='subscription')),
    path('restaurant/', include('apps.restaurant.urls', namespace='restaurant')),
    path('payment/', include('apps.payment.urls', namespace='payment')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
