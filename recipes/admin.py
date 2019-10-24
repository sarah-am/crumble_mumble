from django.contrib import admin
from .models import Recipe, Ingredient, Category, Instruction


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
	inlines = [IngredientInline, InstructionInline]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Instruction)