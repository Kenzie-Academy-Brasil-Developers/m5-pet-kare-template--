from django.db import models


class Trait(models.Model):
    name = models.CharField(max_length=20)
    pets = models.ManyToManyField(
        "pets.Pet",
        related_name="traits"
    )
