from django.urls import path
from recipes import views


urlpatterns = [
    path('', views.recipes_list, name="recipes-list"),
    path('recipe/<recipe_slug>/', views.recipe_details, name="recipe-details"),
    path('create/', views.RecipeCreateView.as_view(), name="create-recipe"),
    path('update/<slug>/', views.RecipeUpdateView.as_view(), name="update-recipe" ),
    path('recipes/my/', views.my_recipes_list, name="my-recipes-list"),
    path('recipes/saved/', views.saved_recipe_list, name="saved-recipe-list"),

    path('save/<recipe_id>/', views.save_recipe, name="save-recipe"),
    path('ingredints/', views.get_ingredients, name="get-ingredients"),

]

