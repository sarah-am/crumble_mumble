from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Recipe(models.Model):
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=150)
	image = models.ImageField(blank=True, null=True)
	description = models.TextField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
	slug = models.SlugField(blank=True)
	

	def __str__(self):
		return self.name


class Ingredient(models.Model):
	name = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name


class Measurement(models.Model):
	GRAMS = "g"
	CUP = "cup"
	TBS = "Tbs"
	TSP = "tsp"
	NOTHING = " "
	MEASURES = [
		(GRAMS,GRAMS),
		(CUP,CUP),
		(TBS,TBS),
		(TSP,TSP),
		(NOTHING,NOTHING)
	]

	amount = models.DecimalField(max_digits=10, decimal_places=2)
	measure = models.CharField(max_length=20, choices=MEASURES)
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="measurements")
	ingredient = models.CharField(max_length=120)



class Instruction(models.Model):
	description = models.TextField()
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="instructions")


class SavedRecipe(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="saved")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_recipes")


def create_slug(instance, new_slug=None):
    slug = slugify (instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Recipe.objects.filter(slug=slug)
    if qs.exists():
        try:
            int(slug[-1])
            if "-" in slug:
                slug_list = slug.split("-")
                new_slug = "%s%s"%(slug[:-1],int(slug_list[-1])+1)
            else:
                new_slug = "%s-1"%(slug)
        except:
            new_slug = "%s-1"%(slug)
        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Recipe)
def generate_slug(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)