from django.forms import ModelForm, Textarea, TextInput
from django.forms.models import inlineformset_factory
from .models import Recipe, Ingredient, Instruction, Measurement


IngredientFormSet = inlineformset_factory(Recipe, Measurement, exclude=['recipe'],
	widgets = {
        'ingredient': TextInput(),
   },
    extra=1, can_delete=True)
InstructionFormSet = inlineformset_factory(Recipe, Instruction, fields=['description'],
	widgets = {
        'description': Textarea(attrs={'cols': 60, 'rows': 2}),
   },
    extra=1, can_delete=True)