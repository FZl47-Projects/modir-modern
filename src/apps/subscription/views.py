from azbankgateways import models as bank_models, default_settings as settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, reverse
from django.utils.translation import gettext as _
from django.views.generic import View, ListView
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404

from apps.payment.models import Order, OrderItem
from .models import Subscription, Subscriber


# Render SubscriptionList view
class SubscriptionListView(LoginRequiredMixin, ListView):
    template_name = 'subscription/list.html'
    model = Subscription
    queryset = Subscription.objects.filter(is_active=True)


# Create SubscriptionOrder view
class CreateSubscriptionOrderView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.get_subscription_time() >= 300:
            messages.info(self.request, _('You cannot active more than 300 days!'))
            return redirect('subscription:subscription_list')

        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        subscription_pk = request.POST.get('pk')
        obj = get_object_or_404(Subscription, pk=subscription_pk)

        # Create order
        order = Order.objects.create(
            user=request.user,
            payable_price=obj.selling_price,
            discount_price=int(obj.price - obj.selling_price),
            callback_url=reverse('subscription:add_subscription')
        )

        OrderItem.objects.create(order=order, item_object=obj)  # Create order item (subscription obj)

        # Save order id via session
        request.session['order_id'] = order.oid
        request.session.modified = True

        return redirect('payment:create_bank')


# Add Subscription view
class AddSubscriptionView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
        if not tracking_code:
            return redirect('payment:callback_failed')

        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        except bank_models.Bank.DoesNotExist:
            return redirect('payment:callback_failed')

        if not bank_record.is_success:
            return redirect('payment:callback_failed')

        return super(AddSubscriptionView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            order = Order.objects.get(oid=request.session['order_id'])
            order_items = OrderItem.objects.filter(order=order)
        except (Order.DoesNotExist, KeyError):
            raise Http404

        # Get user Subscription and add time to it
        subscribe, created = Subscriber.objects.get_or_create(user=order.user)
        for item in order_items:
            subscribe.add_time(item.item_object)

        # Add bank tracking code to order
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
        order.bank_tracking_code = tracking_code
        order.save()

        return redirect('payment:callback_success')
