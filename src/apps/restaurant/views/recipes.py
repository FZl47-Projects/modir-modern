from django.views.generic import TemplateView, FormView, DetailView, View
from django.shortcuts import redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages

from apps.subscription.mixinx import SubscriptionRequiredMixin
from persian_tools import digits, separator
from ..models import (Restaurant, RawMaterial, RecipesCategory, Recipe, RecipeMaterial)
from .. import forms


# Render FoodsRecipes view
class FoodsRecipesView(LoginRequiredMixin, TemplateView):
    template_name = 'restaurant/foods_recipes.html'

    def filter(self, objects):
        cat_filter = self.request.GET.get('filter')
        if cat_filter:
            objects = objects.filter(category__title=cat_filter)

        q = self.request.GET.get('q')
        if q:
            objects = objects.filter(title__icontains=q)

        return objects

    def pagination(self, objects):
        page_number = self.request.GET.get('page')
        paginator = Paginator(objects, 15)
        return paginator.get_page(page_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(user=self.request.user)

        # Get recipes and filter them
        objects = Recipe.objects.filter(category__restaurant=restaurant, is_material=False).order_by('created_at')
        objects = self.filter(objects)
        page_obj = self.pagination(objects)

        context.update({
            'restaurant': restaurant,
            'page_obj': page_obj,
        })

        return context


# Add RecipesCategory view
class AddRecipesCategoryView(SubscriptionRequiredMixin, FormView):
    template_name = 'restaurant/foods_recipes.html'
    form_class = forms.RecipesCategoryForm
    success_url = reverse_lazy('restaurant:recipes')

    def get_form(self, form_class=None):
        data = self.request.POST.copy()
        data.update({'restaurant': Restaurant.objects.get(user=self.request.user)})
        form_class = forms.RecipesCategoryForm(data=data)

        return form_class

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Category successfully added'))
        return super().form_valid(form)


# Delete RecipeCategory view
class DeleteRecipeCategoryView(SubscriptionRequiredMixin, View):
    """ Delete recipe categories based on given title. """
    def post(self, request):
        title = request.POST.get('title')

        try:
            restaurant = Restaurant.objects.get(user=request.user)
            category = RecipesCategory.objects.get(restaurant=restaurant, title=title)
            recipes = Recipe.objects.filter(category=category)

            category.delete()

            for recipe in recipes:
                recipe.calc_final_price()

            messages.success(request, _('Category successfully deleted'))

        except (RecipesCategory.DoesNotExist, Restaurant.DoesNotExist, Restaurant.MultipleObjectsReturned):
            messages.error(request, _('There is an issue. please try again'))

        return redirect('restaurant:recipes')


# Add Recipe view
class AddRecipeView(SubscriptionRequiredMixin, FormView):
    template_name = 'restaurant/foods_recipes.html'
    form_class = forms.RecipeForm
    success_url = reverse_lazy('restaurant:recipes')

    def form_valid(self, form):
        category = form.cleaned_data.get('category')
        if not RecipesCategory.objects.filter(restaurant__user=self.request.user, id=category.id).exists():
            messages.error(self.request, _('There is an issue. please try again'))
            return redirect('restaurant:recipes')

        form.save()

        messages.success(self.request, _('Recipe successfully added'))
        return super().form_valid(form)


# Delete Recipe view
class DeleteRecipeView(SubscriptionRequiredMixin, View):
    """ Delete recipes based on given pk """
    def post(self, request):
        pk = self.request.POST.get('pk')
        obj = get_object_or_404(Recipe, category__restaurant__user=request.user, pk=pk)
        obj.delete()

        messages.success(request, _('Recipe successfully deleted'))
        return redirect('restaurant:recipes')


# RecipeDetails view
class RecipeDetailsView(SubscriptionRequiredMixin, DetailView):
    template_name = 'restaurant/recipe_details.html'
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(user=self.request.user)
        context.update({
            'restaurant': restaurant,
            'raw_materials': RawMaterial.objects.filter(category__restaurant=restaurant),
            'prepared_materials': Recipe.objects.filter(prepared_category__restaurant=restaurant, is_material=True)
        })

        return context

    def get_object(self, queryset=None):
        materials = Recipe.objects.filter(category__restaurant__user=self.request.user, is_material=False)
        obj = get_object_or_404(materials, pk=self.kwargs.get('pk'))
        return obj


# EditRecipe view
class EditRecipeView(SubscriptionRequiredMixin, FormView):
    template_name = 'restaurant/recipe_details.html'
    form_class = forms.RecipeForm

    def get_success_url(self):
        return reverse('restaurant:recipe_details', args=[self.kwargs.get('pk')])

    def get_form(self, form_class=None):
        data = self.request.POST.copy()
        instance = get_object_or_404(Recipe, pk=self.kwargs.get('pk'))
        form_class = forms.RecipeForm(data=data, instance=instance)

        return form_class

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Changes committed successfully'))

        return super().form_valid(form)


# Add RecipeMaterials view
class AddRecipeMaterialsView(SubscriptionRequiredMixin, View):
    """ Add recipe materials one by one with django form. """

    def post(self, request):
        post = request.POST.copy()
        recipe = get_object_or_404(Recipe, category__restaurant__user=request.user, pk=post.get('pk'))

        try:
            materials = post.getlist('raw_material', [])
            prepared_materials = post.getlist('prepared_material', [])
            amount = post.getlist('amount', [])

            for index, item in enumerate(materials):
                if item == 'null':
                    data = {'recipe': recipe, 'prepared_material': prepared_materials[index], 'amount': amount[index]}
                else:
                    data = {'recipe': recipe, 'raw_material': item, 'amount': amount[index]}

                form = forms.AddRecipeMaterialForm(data=data)
                if form.is_valid():
                    form.save()

            messages.success(request, _('Materials added successfully'))

        except (IndexError, TypeError):
            messages.error(request, _('There is an issue. please try again'))

        return redirect(reverse('restaurant:recipe_details', args=[request.POST.get('pk')]))


# Delete RecipeMaterial view
class DeleteRecipeMaterialView(SubscriptionRequiredMixin, View):
    """ Delete raw_material from recipe based on given ID. """
    def post(self, request, pk):
        material_id = request.POST.get('id')
        recipe = get_object_or_404(Recipe, category__restaurant__user=request.user, pk=pk)

        material = get_object_or_404(RecipeMaterial, recipe=recipe, id=material_id)
        material.delete()

        messages.success(request, _('Item successfully deleted'))
        return redirect('restaurant:recipe_details', recipe.pk)


# Get RecipeFinalPrice view
class GetRecipeFinalPriceView(SubscriptionRequiredMixin, View):
    """ Return final price of recipe based on given id. """

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, category__restaurant__user=request.user, pk=pk)
        final_price = digits.convert_to_fa(recipe.calc_final_price())

        return JsonResponse({'price': separator.add(final_price)}, status=200)
