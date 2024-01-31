from django.urls import path
from . import views


app_name = 'restaurant'

urlpatterns = [
    path('materials/', views.RawMaterialsListView.as_view(), name='raw_materials'),
    path('materials/category/add/', views.AddMaterialCategoryView.as_view(), name='add_material_category'),
]
