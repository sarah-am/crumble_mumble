from django.urls import path
from recipes import views


urlpatterns = [
    path('', views.recipes_list, name="recipes-list"),
    path('recipe/<recipe_slug>/', views.recipe_details, name="recipe-details"),
    path('my-recipes/', views.my_recipes_list, name="my-recipes-list"),
    path('create/recipe/', views.RecipeCreateView.as_view(), name="recipe-create"),
    path('update/<slug>/', views.RecipeUpdateView.as_view(), name="update-recipe" ),
	path('recipes/saved/', views.saved_recipe_list, name="saved-recipe-list"),
	path('save/<recipe_id>/', views.save_recipe, name="save-recipe"),
    path('export/<recipe_slug>/', views.export_recipe, name="export-recipe"),

]

