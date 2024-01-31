from django.views.generic import TemplateView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.urls import reverse_lazy

from . import models
from . import forms


# Render RawMaterialsList view
class RawMaterialsListView(LoginRequiredMixin, TemplateView):
    template_name = 'restaurant/raw_materials.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = models.Restaurant.objects.get(user=self.request.user)

        return context


# Add MaterialCategory view
class AddMaterialCategoryView(LoginRequiredMixin, FormView):
    template_name = 'restaurant/raw_materials.html'
    form_class = forms.AddMaterialCategoryForm
    success_url = reverse_lazy('restaurant:raw_materials')

    def get_form(self, form_class=None):
        data = self.request.POST.copy()
        data.update({
            'restaurant': models.Restaurant.objects.get(user=self.request.user)
        })
        form_class = forms.AddMaterialCategoryForm(data=data, files=self.request.FILES)

        return form_class

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
