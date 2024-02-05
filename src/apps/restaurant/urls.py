from django.urls import path
from .views import (
    materials
)


app_name = 'restaurant'

urlpatterns = [
    path('materials/', materials.RawMaterialsListView.as_view(), name='raw_materials'),
    path('materials/category/add/', materials.AddMaterialCategoryView.as_view(), name='add_material_category'),
    path('materials/category/delete/', materials.DeleteMaterialCategoryView.as_view(), name='delete_material_category'),
    path('materials/add/', materials.AddRawMaterialView.as_view(), name='add_raw_materials'),
    path('materials/<int:pk>/edit/', materials.EditRawMaterialView.as_view(), name='edit_raw_materials'),
    path('materials/delete/', materials.DeleteRawMaterialView.as_view(), name='delete_raw_materials'),
    path('materials/<int:pk>/form/', materials.MaterialReduceFormView.as_view(), name='raw_materials_reduce_form'),
]
