from django.shortcuts import redirect
from django.http import Http404


class OrderRequiredMixin:
    """ Only after an order can access this page """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')

        if 'order_id' in request.session:
            del request.session['order_id']
            return super().dispatch(request, *args, **kwargs)

        raise Http404
