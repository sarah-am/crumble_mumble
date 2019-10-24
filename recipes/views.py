from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView

from .models import Recipe, Category, Ingredient, Instruction
from .forms import RecipeForm, IngredientFormSet, InstructionFormSet


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


def my_recipes_list(request):
	return render(request, 'my_recipes_list.html')


class RecipeCreateView(CreateView):
	template_name = 'create_recipe.html'
	form_class = RecipeForm
	success_url = 'recipe-details'

	def get(self, request, *args, **kwargs):
		self.object = None

		form = self.get_form()
		ingredient_form = IngredientFormSet()
		instruction_form = InstructionFormSet()

		return self.render_to_response(
			self.get_context_data(form=form, ingredient_form=ingredient_form, instruction_form=instruction_form)
		)

	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = form_class(request.POST, request.FILES)
		ingredient_form = IngredientFormSet(self.request.POST)
		instruction_form = InstructionFormSet(self.request.POST)
		if (form.is_valid() and ingredient_form.is_valid() and instruction_form.is_valid()):
			return self.form_valid(form, ingredient_form, instruction_form)
		else:
			return self.form_invalid(form, ingredient_form, instruction_form)

	def form_valid(self, form, ingredient_form, instruction_form):
		object = form.save(commit=False)
		object.owner = self.request.user
		object.save()
		ingredient_form.instance = object
		ingredient_form.save()
		instruction_form.instance = object
		instruction_form.save()
		return redirect(self.success_url, object.slug)

	def form_invalid(self, form, ingredient_form, instruction_form):
		return self.render_to_response(
			self.get_context_data(form=form, ingredient_form=ingredient_form, instruction_form=instruction_form)
		)	


class RecipeUpdateView(UpdateView):
	template_name = 'update_recipe.html'
	form_class = RecipeForm
	success_url = 'recipe-details'
	model = Recipe

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = form_class(instance=self.object)
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
			self.get_context_data(form=form, ingredient_form=ingredient_form, instruction_form=instruction_form)
			)

