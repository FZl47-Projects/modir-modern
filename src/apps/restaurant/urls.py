from django.urls import path
from .views import (
    materials, recipes, preparations, menu, profile
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
    path('recipes/material/<int:pk>/edit/', recipes.EditRecipeMaterialsView.as_view(), name='edit_recipe_materials'),
    path('recipes/<int:pk>/material/delete/', recipes.DeleteRecipeMaterialView.as_view(),
         name='delete_recipe_material'),
    path('recipes/<int:pk>/get-price/', recipes.GetRecipeFinalPriceView.as_view(), name='get_recipe_final_price'),

    path('preparations/', preparations.PreparationsView.as_view(), name='preparations'),
    path('preparations/category/add/', preparations.AddPreparationCategoryView.as_view(),
         name='add_preparation_category'),
    path('preparations/category/delete/', preparations.DeletePreparationCategoryView.as_view(),
         name='delete_preparation_category'),
    path('preparations/add/', preparations.AddPreparationView.as_view(), name='add_preparation'),
    path('preparations/delete/', preparations.DeletePreparationView.as_view(), name='delete_preparation'),
    path('preparations/<int:pk>/', preparations.PreparationDetailsView.as_view(), name='preparation_details'),
    path('preparations/<int:pk>/edit', preparations.EditPreparationView.as_view(), name='edit_preparation'),
    path('preparations/material/add/', preparations.AddPreparationMaterialsView.as_view(),
         name='add_preparation_materials'),
    path('preparations/material/<int:pk>/edit/', preparations.EditPreparationMaterialsView.as_view(),
         name='edit_preparation_materials'),
    path('preparatoins/<int:pk>/material/delete/', preparations.DeletePreparationMaterialView.as_view(),
         name='delete_preparation_material'),
    path('preparations/<int:pk>/get-price/', preparations.GetPreparationFinalPriceView.as_view(),
         name='get_preparation_final_price'),

    path('menu/', menu.MenuEngineeringView.as_view(), name='menu_engineering'),
    path('menu/services-fee/update/', menu.UpdateServicesFeeView.as_view(), name='update_services_fee'),
    path('menu/recipe/<int:pk>/update/', menu.UpdateRecipeView.as_view(), name='update_recipe'),

    path('profile/index', profile.Index.as_view(), name='profile_index'),

    path('profile/add-or-update', profile.AddOrUpdateProfileView.as_view(), name='add_or_update_profile'),
    path('profile/fixed-costs/add', profile.AddFixedCostView.as_view(), name='add_fixed_cost'),
    path('profile/fixed-costs/<int:pk>/delete', profile.DeleteFixedCostView.as_view(), name='delete_fixed_cost'),

    path('profile/ongoing-costs/add', profile.AddOngoingCostView.as_view(), name='add_ongoing_cost'),
    path('profile/ongoing-costs/<int:pk>/delete', profile.DeleteOngoingCostView.as_view(), name='delete_ongoing_cost'),

    path('profile/sales-estimate', profile.SalesEstimateView.as_view(), name='profile_sales_estimate'),
    path('profile/add-income-profile', profile.AddIncomeProfileView.as_view(), name='add_income_profile'),
    path('profile/update-income-profile/<int:pk>', profile.UpdateIncomeProfileView.as_view(), name='update_income_profile'),
    path('profile/delete-income-profile/<int:pk>', profile.DeleteIncomeProfileView.as_view(), name='delete_income_profile'),
]
