from django.db import models


class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)
    pet = models.ManyToManyField("pets.Pet", related_name="traits")
