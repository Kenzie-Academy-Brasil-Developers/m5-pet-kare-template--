from django.db import models


class PetSexOptions(models.TextChoices):
    male = "Male"
    female = "Female"
    not_informed = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    sex = models.CharField(
        max_length=50, choices=PetSexOptions.choices, default=PetSexOptions.not_informed
    )
    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, related_name="pets", null=False
    )
