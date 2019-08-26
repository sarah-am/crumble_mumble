from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required

from .models import Recipe, Category, Ingredient, Measurement, SavedRecipe
from .forms import RecipeForm, IngredientForm, IngredientFormSet, InstructionFormSet


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


def recipe_details(request, recipe_slug):
	recipe = Recipe.objects.get(slug=recipe_slug)
	if SavedRecipe.objects.filter(recipe=recipe, user=request.user):
		saved = True
	else:
		saved = False
	context = {
		"recipe" : recipe,
		"saved" : saved
	}
	return render(request, "recipe_details.html", context)


@login_required
def my_recipes_list(request):
	return render(request, "my_recipes_list.html")


@login_required
def saved_recipe_list(request):
	return render(request, "saved_recipe_list.html")


@login_required
def save_recipe(request, recipe_id):
	saved_recipe, created = SavedRecipe.objects.get_or_create(recipe_id=recipe_id, user=request.user)
	if created:
		saved = True
	else:
		saved = False
		saved_recipe.delete()
	return JsonResponse({"saved" : saved})



class RecipeUpdateView(UpdateView):
	template_name = 'update_recipe.html'
	model = Recipe
	form_class = RecipeForm
	success_url = 'recipe-details'

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = form_class(instance=self.get_object())
		ingredient_form = IngredientFormSet(instance=self.object)
		instruction_form = InstructionFormSet(instance=self.object)
		return self.render_to_response(
			self.get_context_data(form=form,
								  ingredient_form=ingredient_form,
								  instruction_form=instruction_form))

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = form_class(request.POST, request.FILES, instance=self.object)
		ingredient_form = IngredientFormSet(self.request.POST, instance=self.object)
		instruction_form = InstructionFormSet(self.request.POST, instance=self.object)
		if (form.is_valid() and ingredient_form.is_valid() and
			instruction_form.is_valid()):
			return self.form_valid(form, ingredient_form, instruction_form)
		else:
			return self.form_invalid(form, ingredient_form, instruction_form)

	def form_valid(self, form, ingredient_form, instruction_form):
		form.save()
		ingredient_form.save()
		instruction_form.save()
		return redirect(self.get_success_url(), self.object.slug)

	def form_invalid(self, form, ingredient_form, instruction_form):
		return self.render_to_response(
			self.get_context_data(form=form,
								  ingredient_form=ingredient_form,
								  instruction_form=instruction_form))



class RecipeCreateView(CreateView):
	template_name = 'create_recipe.html'
	model = Recipe
	form_class = RecipeForm
	success_url = 'recipe-details'


	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		ingredient_form = IngredientFormSet()
		instruction_form = InstructionFormSet()
		return self.render_to_response(
			self.get_context_data(form=form,
								  ingredient_form=ingredient_form,
								  instruction_form=instruction_form))

	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = form_class(request.POST, request.FILES)
		ingredient_form = IngredientFormSet(self.request.POST)
		instruction_form = InstructionFormSet(self.request.POST)
		if (form.is_valid() and ingredient_form.is_valid() and
			instruction_form.is_valid()):
			return self.form_valid(form, ingredient_form, instruction_form)
		else:
			return self.form_invalid(form, ingredient_form, instruction_form)

	def form_valid(self, form, ingredient_form, instruction_form):
		self.object = form.save(commit=False)
		self.object.owner = self.request.user
		self.object.save()
		ingredient_form.instance = self.object
		ingredient_form.save()
		instruction_form.instance = self.object
		instruction_form.save()
		return redirect(self.get_success_url(), self.object.slug)

	def form_invalid(self, form, ingredient_form, instruction_form):
		return self.render_to_response(
			self.get_context_data(form=form,
								  ingredient_form=ingredient_form,
								  instruction_form=instruction_form))


@login_required
def get_ingredients(request):
	response = [ingredient.name for ingredient in Ingredient.objects.all()]
	return JsonResponse(response, safe=False)
	