from django.views.generic import TemplateView, FormView, DetailView, View
from django.shortcuts import redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages

from apps.subscription.mixinx import SubscriptionRequiredMixin
from persian_tools import digits, separator
from ..models import (Restaurant, RawMaterial, PreparedMaterialCategory, Recipe, RecipeMaterial)
from .. import forms


# Render Preparations view
class PreparationsView(LoginRequiredMixin, TemplateView):
    template_name = 'restaurant/preparations.html'

    def filter(self, objects):
        cat_filter = self.request.GET.get('filter')
        if cat_filter:
            objects = objects.filter(prepared_category__title=cat_filter)

        q = self.request.GET.get('q')
        if q:
            objects = objects.filter(title__icontains=q)

        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(user=self.request.user)

        # Get items and filter them
        objects = Recipe.objects.filter(prepared_category__restaurant=restaurant, is_material=True)
        objects = self.filter(objects)

        context.update({
            'restaurant': restaurant,
            'objects': objects,
        })

        return context


# Add PreparationCategory view
class AddPreparationCategoryView(SubscriptionRequiredMixin, FormView):
    template_name = 'restaurant/preparations.html'
    form_class = forms.PreparedMaterialCategoryForm
    success_url = reverse_lazy('restaurant:preparations')

    def get_form(self, form_class=None):
        data = self.request.POST.copy()
        data.update({'restaurant': Restaurant.objects.get(user=self.request.user)})
        form_class = forms.PreparedMaterialCategoryForm(data=data)

        return form_class

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Category successfully added'))
        return super().form_valid(form)


# Delete PreparationCategory view
class DeletePreparationCategoryView(SubscriptionRequiredMixin, View):
    """ Delete prepared material categories based on given title. """

    def post(self, request):
        obj_id = request.POST.get('id')
        try:
            restaurant = Restaurant.objects.get(user=request.user)
            category = PreparedMaterialCategory.objects.get(restaurant=restaurant, id=obj_id)
            recipes = Recipe.objects.filter(prepared_category=category)

            category.delete()

            for recipe in recipes:
                recipe.calc_final_price()

            messages.success(request, _('Category successfully deleted'))

        except (PreparedMaterialCategory.DoesNotExist, Restaurant.DoesNotExist, Restaurant.MultipleObjectsReturned):
            messages.error(request, _('There is an issue. please try again'))

        return redirect('restaurant:preparations')


# Add Preparation view
class AddPreparationView(SubscriptionRequiredMixin, FormView):
    template_name = 'restaurant/preparations.html'
    form_class = forms.PreparationForm
    success_url = reverse_lazy('restaurant:preparations')

    def form_valid(self, form):
        category = form.cleaned_data.get('prepared_category')

        if not PreparedMaterialCategory.objects.filter(restaurant__user=self.request.user, id=category.id).exists():
            messages.error(self.request, _('There is an issue. please try again'))
            return redirect('restaurant:preparations')

        form.save(commit=False)

        messages.success(self.request, _('Item successfully added'))
        return super().form_valid(form)


# Delete Preparation view
class DeletePreparationView(SubscriptionRequiredMixin, View):
    """ Delete material preparation based on given pk """

    def post(self, request):
        pk = self.request.POST.get('pk')
        obj = get_object_or_404(Recipe, prepared_category__restaurant__user=request.user, pk=pk, is_material=True)
        obj.delete()

        messages.success(request, _('Item successfully deleted'))
        return redirect('restaurant:preparations')


# PreparationDetails view
class PreparationDetailsView(SubscriptionRequiredMixin, DetailView):
    template_name = 'restaurant/preparation_details.html'
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(user=self.request.user)
        context.update({
            'restaurant': restaurant,
            'raw_materials': RawMaterial.objects.filter(category__restaurant=restaurant),
        })

        return context

    def get_object(self, queryset=None):
        materials = Recipe.objects.filter(prepared_category__restaurant__user=self.request.user, is_material=True)
        obj = get_object_or_404(materials, pk=self.kwargs.get('pk'))
        return obj


# EditPreparation view
class EditPreparationView(SubscriptionRequiredMixin, FormView):
    template_name = 'restaurant/preparation_details.html'
    form_class = forms.PreparationForm

    def get_success_url(self):
        return reverse('restaurant:preparation_details', args=[self.kwargs.get('pk')])

    def get_form(self, form_class=None):
        data = self.request.POST.copy()
        instance = get_object_or_404(Recipe, pk=self.kwargs.get('pk'))
        form_class = forms.PreparationForm(data=data, instance=instance)

        return form_class

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Changes committed successfully'))

        return super().form_valid(form)


# Add PreparationMaterials view
class AddPreparationMaterialsView(SubscriptionRequiredMixin, View):
    """ Add preparation materials one by one with django form """

    def post(self, request):
        post = request.POST.copy()
        recipe = get_object_or_404(Recipe, prepared_category__restaurant__user=request.user, pk=post.get('pk'),
                                   is_material=True)

        try:
            materials = post.getlist('raw_material', [])
            amount = post.getlist('amount', [])

            for index, item in enumerate(materials):
                data = {'recipe': recipe, 'raw_material': item, 'amount': amount[index]}

                form = forms.AddPreparationMaterialForm(data=data)
                if form.is_valid():
                    form.save()

            messages.success(request, _('Materials added successfully'))

        except (IndexError, TypeError):
            messages.error(request, _('There is an issue. please try again'))

        return redirect('restaurant:preparation_details', request.POST.get('pk'))


# Edit PreparationMaterials view
class EditPreparationMaterialsView(SubscriptionRequiredMixin, View):
    """ Edit preparation materials one by one with django form """
    def post(self, request, pk):
        recipe_material = get_object_or_404(RecipeMaterial, recipe__prepared_category__restaurant__user=request.user, pk=pk)
        form = forms.UpdateRecipeMaterialForm(data=request.POST, instance=recipe_material)
        if not form.is_valid():
            messages.error(request, _('Please enter field correctly'))
            return redirect('restaurant:preparation_details', request.POST.get('pk'))
        form.save()
        messages.success(request, _('Material updated successfully'))
        return redirect('restaurant:preparation_details', request.POST.get('pk'))


# Delete PreparationMaterial view
class DeletePreparationMaterialView(SubscriptionRequiredMixin, View):
    """ Delete raw_material from preparation based on given ID. """

    def post(self, request, pk):
        material_id = request.POST.get('id')
        recipe = get_object_or_404(Recipe, prepared_category__restaurant__user=request.user, pk=pk)

        material = get_object_or_404(RecipeMaterial, recipe=recipe, id=material_id)
        material.delete()

        messages.success(request, _('Item successfully deleted'))
        return redirect('restaurant:preparation_details', recipe.pk)


# Get PreparationFinalPrice view
class GetPreparationFinalPriceView(SubscriptionRequiredMixin, View):
    """ Return final price of prepared materials based on given id. """

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, prepared_category__restaurant__user=request.user, pk=pk)
        final_price = digits.convert_to_fa(recipe.calc_final_price())

        return JsonResponse({'price': separator.add(final_price)}, status=200)
