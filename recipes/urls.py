from django.urls import path
from recipes import views


urlpatterns = [
    path('', views.recipes_list, name="recipes-list"),
    path('recipe/<recipe_slug>/', views.recipe_details, name="recipe-details"),
    path('my-recipes/', views.my_recipes_list, name="my-recipes-list"),
]

