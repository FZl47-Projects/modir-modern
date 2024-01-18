from django.utils.translation import gettext as _
from django.shortcuts import redirect


# LogoutRequired mixin
class LogoutRequiredMixin:
    """ Anonymous users access only """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        return super().dispatch(request, *args, **kwargs)


