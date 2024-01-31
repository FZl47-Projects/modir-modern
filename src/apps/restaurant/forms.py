from django.utils.translation import gettext as _
from django import forms

from .models import RawMaterialCategory


# AddMaterialCategory form
class AddMaterialCategoryForm(forms.ModelForm):
    class Meta:
        model = RawMaterialCategory
        fields = ('restaurant', 'title')
