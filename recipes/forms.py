from django.forms import ModelForm, Textarea
from django.forms.models import inlineformset_factory
from .models import Recipe, Instruction, Ingredient

class RecipeForm(ModelForm):
	class Meta:
		model = Recipe
		exclude = ['owner', 'slug']


IngredientFormSet = inlineformset_factory(
	Recipe, Ingredient, exclude=['recipe'], 
	extra=1, 
	can_delete=True
	)

InstructionFormSet = inlineformset_factory(
	Recipe, 
	Instruction, 
	fields=['description'],
	widgets = { 'description': Textarea(attrs={'cols': 60, 'rows': 2})},
    extra=1,
    can_delete=True
    )