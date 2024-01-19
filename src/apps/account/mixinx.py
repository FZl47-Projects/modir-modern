from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib import messages


class LogoutRequiredMixin:
    """ Anonymous users access only """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        return super().dispatch(request, *args, **kwargs)


class AccessRequiredMixin:
    """ Allow access only to given roles. """
    roles = []

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('account:login')

        if request.user.accesses.filter(title__in=self.roles).exists():
            return super().dispatch(request, *args, **kwargs)

        messages.error(request, _('You do not have permission to access this page!'))

        referer_url = request.META.get('HTTP_REFERER')
        return redirect(referer_url or '/')
