from django.contrib import admin
from .models import Recipe, Ingredient, Category, Measurement, Instruction

class MeasurementInline(admin.TabularInline):
    model = Measurement
    extra = 1


class MethodInline(admin.TabularInline):
    model = Instruction
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
	inlines = [MeasurementInline, MethodInline]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category)
admin.site.register(Ingredient)