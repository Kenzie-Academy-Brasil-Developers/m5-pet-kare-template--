from django.db import models


class PetChoices(models.TextChoices):
    Male = "Male"
    Female = "Female"
    Not_Informed = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=20, choices=PetChoices.choices,
                           default=PetChoices.Not_Informed)

    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.PROTECT,
        related_name="pets"
    )