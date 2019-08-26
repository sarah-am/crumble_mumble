from django.contrib import admin
from .models import Recipe, Ingredient, Category, Instruction


admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Instruction)