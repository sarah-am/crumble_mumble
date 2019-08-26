from django.forms import ModelForm, Textarea, TextInput
from django.forms.models import inlineformset_factory
from .models import Recipe, Ingredient, Instruction, Measurement


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ['slug', 'owner']

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"


IngredientFormSet = inlineformset_factory(Recipe, Measurement, exclude=['recipe'],
	widgets = {
        'ingredient': TextInput(),
   },
    extra=1)
InstructionFormSet = inlineformset_factory(Recipe, Instruction, fields=['description'],
	widgets = {
        'description': Textarea(attrs={'cols': 60, 'rows': 2}),
   },
    extra=1)