from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.utils.translation import gettext as _
from django.shortcuts import redirect, render
from django.contrib import messages

from azbankgateways.exceptions import AZBankGatewaysException
from azbankgateways import bankfactories
from .mixins import OrderRequiredMixin
from .models import Order


# Create BankGateway view
class CreateBankGatewayView(LoginRequiredMixin, View):
    def get(self, request):
        referer_url = request.META.get('HTTP_REFERER')

        try:
            order_id = request.session['order_id']
            order = Order.objects.get(oid=order_id)
        except (Order.DoesNotExist, KeyError):
            messages.error(request, _('There was a problem connecting to the bank gateway. Please try again'))
            return redirect(referer_url) if referer_url else redirect('public:index')

        user_mobile_number = str(request.user.phone_number)
        factory = bankfactories.BankFactory()
        try:
            bank = factory.auto_create()
            bank.set_request(request)
            bank.set_amount(int(order.payable_price))
            bank.set_client_callback_url(order.callback_url)
            bank.set_mobile_number(user_mobile_number)

            bank_record = bank.ready()

            context = bank.get_gateway()
            return render(request, 'payment/redirect_to_bank.html', context=context)

        except AZBankGatewaysException as e:
            messages.error(request, _('There was a problem connecting to the bank gateway. Please try again'))
            return redirect(referer_url) if referer_url else redirect('public:index')


# Render CallBackSuccess view
class CallBackSuccessView(TemplateView):
    template_name = 'payment/callback_success.html'


# Render CallBackFailed view
class CallBackFailedView(OrderRequiredMixin, TemplateView):
    template_name = 'payment/callback_failed.html'
