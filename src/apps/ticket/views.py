from django.views.generic import FormView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Ticket
from . import forms


# Render TicketList view
class TicketListView(LoginRequiredMixin, ListView):
    template_name = 'ticket/ticket_list.html'
    model = Ticket
    context_object_name = 'tickets'

    def get_queryset(self):
        queryset = Ticket.objects.filter(is_active=True, user=self.request.user)
        return queryset


# Render TicketCreate view
class TicketCreateView(LoginRequiredMixin, FormView):
    template_name = 'ticket/tickets_create.html'
    form_class = forms.CreateTicketForm
    success_url = reverse_lazy('ticket:ticket_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.filter(is_active=True, user=self.request.user)
        return context

    def get_form(self, form_class=None):
        data = self.request.POST.copy()
        data.update({'user': self.request.user.id})
        form_class = forms.CreateTicketForm(data=data, files=self.request.FILES)

        return form_class

    def form_valid(self, form):
        form.save()

        messages.success(self.request, _('Ticket sent successfully'))
        return super().form_valid(form)


# Render TicketDetails view
class TicketDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'ticket/ticket_details.html'
    model = Ticket
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.filter(is_active=True, user=self.request.user)

        return context


# CreateMessage view
class CreateMessageView(LoginRequiredMixin, FormView):
    template_name = 'ticket/ticket_details.html'
    form_class = forms.CreateMessageForm

    def get_success_url(self):
        return reverse('ticket:ticket_details', args=[self.kwargs.get('pk')])

    def get_form(self, form_class=None):
        data = self.request.POST.copy()
        data.update({'user': self.request.user.id, 'ticket': self.kwargs.get('pk')})
        form_class = forms.CreateMessageForm(data=data, files=self.request.FILES)

        return form_class

    def form_valid(self, form):
        form.save()

        messages.success(self.request, _('Message sent successfully'))
        return super().form_valid(form)
