from django.utils.translation import gettext as _
from django import forms

from .models import Ticket, Messages


# CreateTicket form
class CreateTicketForm(forms.ModelForm):
    text = forms.CharField(max_length=512, required=True, widget=forms.Textarea)
    file = forms.FileField(required=False, widget=forms.FileInput)

    class Meta:
        model = Ticket
        fields = ('user', 'title', 'type')

    def save(self, commit=True):
        obj = super().save(commit)
        ticket_text = self.cleaned_data.get('text')
        ticket_file = self.cleaned_data.get('file')

        Messages.objects.create(
            ticket=obj,
            user=obj.user,
            text=ticket_text,
            file=ticket_file)

        return obj


# CreateMessage form
class CreateMessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ('ticket', 'user', 'text', 'file')
