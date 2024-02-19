from django.shortcuts import get_object_or_404, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F, PositiveIntegerField
from django.views.generic import TemplateView, View, FormView
from django.utils.translation import gettext as _
from django.db.models.functions import Cast
from django.core.paginator import Paginator
from django.contrib import messages

from apps.subscription.mixinx import SubscriptionRequiredMixin
from ..models import (Restaurant, Recipe)
from .. import forms


# Render MenuEngineering view
class MenuEngineeringView(LoginRequiredMixin, TemplateView):
    template_name = 'restaurant/menu_engineering.html'

    def filter(self, objects):
        cat_filter = self.request.GET.get('filter')
        if cat_filter:
            objects = objects.filter(category__title=cat_filter)

        return objects

    def pagination(self, objects):
        page_number = self.request.GET.get('page')
        paginator = Paginator(objects, 15)
        return paginator.get_page(page_number)

    def get_context_data(self, object_list=None, **kwargs):
        context = super(MenuEngineeringView, self).get_context_data(**kwargs)
        restaurant = get_object_or_404(Restaurant, user=self.request.user)

        # Get recipes and filter them
        objects = Recipe.objects.filter(category__restaurant=restaurant, is_material=False).order_by('created_at')
        objects = self.filter(objects)
        page_obj = self.pagination(objects)

        try:
            context.update({
                'restaurant': restaurant,
                'page_obj': page_obj,
                'objects': objects.aggregate(
                    total_final_price=Sum('final_price'),
                    total_service_price=Sum('service_price'),
                    total_price_with_factor=Sum('price_with_factor'),
                    total_menu_price=Sum('menu_price'),
                    total_item_profit=Sum('item_profit'),
                    total_number_sold=Sum('number_sold'),
                    total_total_sales=Sum('total_sales'),
                    total_total_cost=Sum('total_cost'),
                    total_total_profit=Sum('total_profit'),
                    each_item_profit_avg=Sum('total_profit') / Sum('number_sold'),
                ),
                'each_item_percentage_share': 0.7 / (objects.count() or 1),
            })
        except ZeroDivisionError:
            context.update({
                'restaurant': restaurant,
                'page_obj': page_obj,
                'objects': objects.aggregate(
                    total_final_price=Sum('final_price'),
                    total_service_price=Sum('service_price'),
                    total_price_with_factor=Sum('price_with_factor'),
                    total_menu_price=Sum('menu_price'),
                    total_item_profit=Sum('item_profit'),
                    total_number_sold=Sum('number_sold'),
                    total_total_sales=Sum('total_sales'),
                    total_total_cost=Sum('total_cost'),
                    total_total_profit=Sum('total_profit'),
                    each_item_profit_avg=Sum('total_profit') / 1,
                ),
                'each_item_percentage_share': 0.7 / (objects.count() or 1),
            })

        return context


# Update Restaurant ServicesFee view
class UpdateServicesFeeView(SubscriptionRequiredMixin, View):
    """ Update restaurant services fee """

    def get_redirect_url(self, request):
        return reverse('restaurant:menu_engineering') + f'?filter={request.GET.get("filter")}'

    def post(self, request):
        fee = int(request.POST.get('services_fee'))
        restaurant = get_object_or_404(Restaurant, user=self.request.user)

        restaurant.services_fee = fee
        restaurant.save()

        # Update recipes service_prices based on services_fee
        recipes = Recipe.objects.filter(category__restaurant=restaurant, is_material=False)
        recipes.update(service_price=Cast(F('final_price') * (fee / 100), output_field=PositiveIntegerField()))

        messages.success(request, _('Services fee updated'))
        return redirect(self.get_redirect_url(request))  # Redirect with GET parameters


# UpdateRecipe view
class UpdateRecipeView(SubscriptionRequiredMixin, FormView):
    template_name = 'restaurant/menu_engineering.html'
    form_class = forms.UpdateRecipeForm

    def get_success_url(self):
        return reverse('restaurant:menu_engineering') + f'?filter={self.request.GET.get("filter")}&page={self.request.GET.get("page")}'

    def get_form(self, form_class=None):
        obj = get_object_or_404(Recipe, category__restaurant__user=self.request.user, pk=self.kwargs.get('pk'))
        return forms.UpdateRecipeForm(data=self.request.POST, instance=obj)
    
    def form_valid(self, form):
        form.save(commit=False)
        
        messages.success(self.request, _('Item updated successfully'))
        return super().form_valid(form)
