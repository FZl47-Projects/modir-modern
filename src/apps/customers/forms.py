from django import forms
from .models import CustomerSurvey, Counseling


# CustomerSurveys form
class CustomerSurveyForm(forms.ModelForm):
    class Meta:
        model = CustomerSurvey
        fields = "__all__"


# Counseling form
class CounselingForm(forms.ModelForm):
    class Meta:
        model = Counseling
        fields = "__all__"
