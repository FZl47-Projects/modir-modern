from django.urls import path
from .views import (
    materials, recipes
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

    path('recipes/', recipes.FoodsRecipesView.as_view(), name='recipes'),
    path('recipes/category/add/', recipes.AddRecipesCategoryView.as_view(), name='add_recipe_category'),
    path('recipes/category/delete/', recipes.DeleteRecipeCategoryView.as_view(), name='delete_recipe_category'),
    path('recipes/add/', recipes.AddRecipeView.as_view(), name='add_recipe'),
    path('recipes/delete/', recipes.DeleteRecipeView.as_view(), name='delete_recipe'),
    path('recipes/<int:pk>/', recipes.RecipeDetailsView.as_view(), name='recipe_details'),
    path('recipes/<int:pk>/edit/', recipes.EditRecipeView.as_view(), name='edit_recipe'),
    path('recipes/material/add/', recipes.AddRecipeMaterialsView.as_view(), name='add_recipe_materials'),
    path('recipes/<int:pk>/material/delete/', recipes.DeleteRecipeMaterialView.as_view(), name='delete_recipe_material'),
]
