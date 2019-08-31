from django.urls import path
from recipes import views


urlpatterns = [
    path('', views.recipes_list, name="recipes-list"),
    path('recipe/<recipe_slug>/', views.recipe_details, name="recipe-details"),
    path('create/recipe/', views.RecipeCreateView.as_view(), name="recipe-create"),
    path('update/<slug>/', views.RecipeUpdateView.as_view(), name="update-recipe" ),
]

