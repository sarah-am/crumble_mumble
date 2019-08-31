from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import Recipe, Instruction, Ingredient


class RecipeForm(ModelForm):
	class Meta:
		model = Recipe
		exclude = ['owner', 'slug']


IngredientFormSet = inlineformset_factory(Recipe, Ingredient, exclude=['recipe'], extra=1, can_delete=True)
InstructionFormSet = inlineformset_factory(Recipe, Instruction, fields=['description'], extra=1, can_delete=True)