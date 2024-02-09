from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django import forms

from .models import (RawMaterialCategory, RawMaterial, RecipesCategory, Recipe, RecipeMaterial)


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
        fields = ('category', 'title', 'use_for', 'price')


# ReduceRawMaterial form
class ReduceRawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        exclude = ('category', 'title', 'price', 'raw_usable_quantity_cost', 'baked_usable_quantity_cost',
                   'raw_usable_quantity_cost_per_press', 'baked_usable_quantity_cost_per_press',
                   'number_of_raw_use', 'number_of_baked_use')

    def save(self, commit=True):
        obj = super().save(commit)

        # Calculate the rest fields and save them
        obj.raw_usable_quantity_cost = (obj.price * obj.delivery_weight) / obj.edible_cleaned_weight if obj.delivery_weight else 0
        obj.baked_usable_quantity_cost = (obj.price * obj.delivery_weight) / obj.salable_weight if obj.delivery_weight else 0

        obj.raw_usable_quantity_cost_per_press = obj.raw_usable_quantity_cost * obj.quantity_raw_press
        obj.baked_usable_quantity_cost_per_press = obj.raw_usable_quantity_cost * obj.quantity_baked_press

        obj.number_of_raw_use = obj.edible_cleaned_weight / obj.quantity_raw_press if obj.quantity_raw_press else 0
        obj.number_of_baked_use = obj.salable_weight / obj.quantity_baked_press if obj.quantity_baked_press else 0

        obj.save()
        return obj


# -------------------------------------------------------------------


# Add RecipesCategory form
class RecipesCategoryForm(forms.ModelForm):
    class Meta:
        model = RecipesCategory
        fields = ('restaurant', 'title')


# Recipe form
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'category', 'preparation')

    def save(self, commit=True):
        obj = super().save(commit)
        obj.save()

        return obj


# AddRecipeMaterial form
class AddRecipeMaterialForm(forms.ModelForm):
    class Meta:
        model = RecipeMaterial
        fields = ('recipe', 'raw_material', 'prepared_material', 'amount')


# -----------------------------------------

# Preparation form
class PreparationForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('category', 'title', 'preparation', 'is_material')

    def save(self, commit=True):
        obj = super().save(commit)
        obj.is_material = True
        obj.save()

        return obj


# AddPreparationMaterial form
class AddPreparationMaterialForm(forms.ModelForm):
    class Meta:
        model = RecipeMaterial
        fields = ('recipe', 'raw_material', 'amount')
