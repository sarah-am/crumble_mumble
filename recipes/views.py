from django.shortcuts import render
from .models import Recipe, Category


def recipes_list(request):
	if request.GET.get('q'):
		recipes = Recipe.objects.filter(name__contains=request.GET.get('q'))
	else:
		recipes = Recipe.objects.all()

	categories = Category.objects.all()
	context = {
		"recipes" : recipes,
		"categories" :categories
	}
	return render(request, "recipes_list.html", context)





	