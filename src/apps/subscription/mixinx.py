from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib import messages


class SubscriptionRequiredMixin:
    """ Subscription required to access page """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')

        if request.user.has_subscription():
            return super().dispatch(request, *args, **kwargs)

        messages.error(request, _('You need to purchase subscription to use this service.'))

        referer_url = request.META.get('HTTP_REFERER')
        return redirect(referer_url) if referer_url else redirect('public:index')

