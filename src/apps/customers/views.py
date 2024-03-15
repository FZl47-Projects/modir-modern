from django.views.generic import ListView, FormView, DetailView
from django.shortcuts import redirect, get_object_or_404
from apps.restaurant.models import Restaurant, Recipe


# Render Customer ServicesList view
class ServicesListView(DetailView):
    template_name = 'customers/services_list.html'
    model = Restaurant

    def get_object(self, queryset=None):
        obj = get_object_or_404(Restaurant, pk=self.request.GET.get('code'))
        return obj


# Render Customer DigitalMenu view
class DigitalMenuView(ListView):
    template_name = 'customers/digital_menu.html'
    model = Restaurant

    def filter(self, restaurant, objects):
        category = self.request.GET.get('category')
        if category:
            objects = objects.filter(category__title=category)
        else:
            objects = objects.filter(category=restaurant.recipes_categories.first())

        return objects

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs.get('pk'))
        queryset = Recipe.objects.filter(category__restaurant=restaurant)

        queryset = self.filter(restaurant, queryset)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'restaurant': get_object_or_404(Restaurant, pk=self.kwargs.get('pk'))
        })

        return context
