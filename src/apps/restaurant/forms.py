from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django import forms

from .models import (RawMaterialCategory, RawMaterial, RecipesCategory, PreparedMaterialCategory, Recipe,
                     RecipeMaterial, RestaurantProfile,
                     FixedCosts, OngoingCosts, IncomeAndCostsProfile
                     )


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
        obj.calculate_results()

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


# UpdateRecipeMaterialForm form
class UpdateRecipeMaterialForm(forms.ModelForm):
    class Meta:
        model = RecipeMaterial
        fields = ('amount',)


# -----------------------------------------

# Add PreparedMaterialCategory form
class PreparedMaterialCategoryForm(forms.ModelForm):
    class Meta:
        model = PreparedMaterialCategory
        fields = ('restaurant', 'title')


# Preparation form
class PreparationForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('prepared_category', 'title', 'preparation', 'is_material')

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


# ----------------------------------------------

# Update Recipe form
class UpdateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('factor', 'menu_price', 'number_sold')

    def save(self, commit=True):
        obj = super().save(commit)
        obj.calculate_results(save=False)
        obj.save()

        return obj


class RestaurantProfileForm(forms.ModelForm):
    class Meta:
        model = RestaurantProfile
        fields = '__all__'


class AddFixedCostForm(forms.ModelForm):
    class Meta:
        model = FixedCosts
        fields = '__all__'


class AddOngoingCostForm(forms.ModelForm):
    class Meta:
        model = OngoingCosts
        fields = '__all__'


class AddIncomeProfile(forms.ModelForm):
    class Meta:
        model = IncomeAndCostsProfile
        fields = '__all__'


class UpdateIncomeProfile(forms.ModelForm):
    class Meta:
        model = IncomeAndCostsProfile
        exclude = ('restaurant_profile',)
