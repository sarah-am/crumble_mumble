from django.shortcuts import render
from .models import Recipe, Category


def recipes_list(request):

	recipes = Recipe.objects.filter(private=False)
	categories = Category.objects.all()

	context = {
		"recipes" : recipes,
		"categories" :categories
	}
	return render(request, "recipes_list.html", context)


def recipe_details(request, recipe_slug):
	recipe = Recipe.objects.get(slug=recipe_slug)

	context = {
		"recipe" : recipe,
	}
	return render(request, "recipe_details.html", context)
