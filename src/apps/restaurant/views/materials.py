from django.views.generic import TemplateView, FormView, View
from django.shortcuts import redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib import messages

from apps.core.utils import toast_form_errors
from apps.restaurant.models import (Restaurant, RawMaterialCategory, RawMaterial)
from .. import forms


# Render RawMaterialsList view
class RawMaterialsListView(LoginRequiredMixin, TemplateView):
    template_name = 'restaurant/raw_materials.html'

    def filter(self, objects):
        # TODO: Add search for materials
        cat_filter = self.request.GET.get('filter')
        if cat_filter:
            objects = objects.filter(category__title=cat_filter)
        return objects

    def pagination(self, objects):
        page_number = self.request.GET.get('page')
        paginator = Paginator(objects, 30)
        return paginator.get_page(page_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(user=self.request.user)

        # Get raw materials and filter them
        materials = RawMaterial.objects.filter(category__restaurant=restaurant).order_by('created_at')
        materials = self.filter(materials)
        page_obj = self.pagination(materials)

        context.update({
            'restaurant': restaurant,
            'page_obj': page_obj,
        })
        return context


# Add MaterialCategory view
class AddMaterialCategoryView(LoginRequiredMixin, FormView):
    template_name = 'restaurant/raw_materials.html'
    form_class = forms.AddMaterialCategoryForm
    success_url = reverse_lazy('restaurant:raw_materials')

    def get_form(self, form_class=None):
        data = self.request.POST.copy()
        data.update({
            'restaurant': Restaurant.objects.get(user=self.request.user)
        })
        form_class = forms.AddMaterialCategoryForm(data=data, files=self.request.FILES)

        return form_class

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return redirect('restaurant:raw_materials')


# Delete MaterialCategory view
class DeleteMaterialCategoryView(LoginRequiredMixin, View):
    """ Delete raw material category based on pk """
    def post(self, request):
        title = request.POST.get('title')

        try:
            restaurant = Restaurant.objects.get(user=request.user)
            obj = RawMaterialCategory.objects.get(restaurant=restaurant, title=title)
            obj.delete()
            messages.success(request, _('Category successfully deleted'))

        except (RawMaterialCategory.DoesNotExist, Restaurant.DoesNotExist):
            messages.error(request, _('There is an issue. please try again'))

        return redirect('restaurant:raw_materials')


# Add RawMaterial view
class AddRawMaterialView(LoginRequiredMixin, FormView):
    template_name = 'restaurant/raw_materials.html'
    form_class = forms.RawMaterialForm
    success_url = reverse_lazy('restaurant:raw_materials')

    def form_valid(self, form):
        post = self.request.POST.copy()
        try:
            titles = post.getlist('title', [])
            uses = post.getlist('use_for', [])
            prices = post.getlist('price', [])
            categories = post.getlist('category', [])

            for index, item in enumerate(titles):
                data = {
                    'title': item,
                    'use_for': uses[index],
                    'price': prices[index],
                    'category': categories[index]
                }
                form = forms.RawMaterialForm(data=data)

                if form.is_valid():
                    form.save()

            messages.success(self.request, _('Raw materials added successfully'))

        except (IndexError, TypeError):
            messages.error(self.request, _('There is an issue. please try again'))

        return super().form_valid(form)


# Edit RawMaterial view
class EditRawMaterialView(LoginRequiredMixin, FormView):
    template_name = 'restaurant/raw_materials.html'
    form_class = forms.RawMaterialForm
    success_url = reverse_lazy('restaurant:raw_materials')

    def get_form(self, form_class=None):
        data = self.request.POST.copy()
        instance = get_object_or_404(RawMaterial, pk=self.kwargs.get('pk'))

        return forms.RawMaterialForm(data=data, instance=instance)

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        restaurant = Restaurant.objects.get(user=self.request.user)
        
        if not RawMaterial.objects.filter(category__restaurant=restaurant, pk=pk).exists():
            return self.form_invalid(form)
        form.save()

        messages.success(self.request, _('Item successfully modified'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('There is an issue. please try again'))
        return redirect('restaurant:raw_materials')


# Delete RawMaterial view
class DeleteRawMaterialView(LoginRequiredMixin, View):
    """ Delete raw material objects based on pk """
    def post(self, request):
        pk = self.request.POST.get('pk')

        restaurant = Restaurant.objects.get(user=self.request.user)
        obj = get_object_or_404(RawMaterial, category__restaurant=restaurant, pk=pk)
        obj.delete()

        messages.success(self.request, _("Item deleted successfully"))
        return redirect('restaurant:raw_materials')


# Render ReduceForm view
class MaterialReduceFormView(LoginRequiredMixin, FormView):
    template_name = 'restaurant/reduce_form.html'
    model = RawMaterial
    form_class = forms.ReduceRawMaterialForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = RawMaterial.objects.filter(category__restaurant__user=self.request.user)
        context['object'] = get_object_or_404(queryset, pk=self.kwargs.get('pk'))

        return context

    def get_success_url(self):
        return reverse('restaurant:raw_materials_reduce_form', args=[self.kwargs.get('pk')])

    def get_form(self, form_class=None):
        data = self.request.POST.copy()
        instance = get_object_or_404(RawMaterial, pk=self.kwargs.get('pk'))

        return forms.ReduceRawMaterialForm(data=data, instance=instance)

    def form_valid(self, form):
        form.save(commit=False)
        messages.success(self.request, _('Items saved successfully. You can see results down below'))

        return super().form_valid(form)
