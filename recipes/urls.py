from django.urls import path
from recipes import views


urlpatterns = [
    path('', views.recipes_list, name="recipes-list"),
    path('recipe/<recipe_slug>/', views.recipe_details, name="recipe-details"),
]

