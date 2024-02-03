from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django import forms

from .models import (RawMaterialCategory, RawMaterial)


# AddMaterialCategory form
class AddMaterialCategoryForm(forms.ModelForm):
    class Meta:
        model = RawMaterialCategory
        fields = ('restaurant', 'title')

    def clean(self):
        restaurant = self.cleaned_data.get('restaurant')
        title = self.cleaned_data.get('title')

        if RawMaterialCategory.objects.filter(restaurant=restaurant, title=title).exists():
            raise ValidationError(_('This category is already exists'), code='OBJECT-EXISTS')

        return self.cleaned_data


# RawMaterial form
class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = ('category', 'title', 'price')
