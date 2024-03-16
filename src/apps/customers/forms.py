from django import forms
from .models import CustomerSurvey


# CustomerSurveys form
class CustomerSurveyForm(forms.ModelForm):
    class Meta:
        model = CustomerSurvey
        fields = "__all__"
