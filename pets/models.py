from django.db import models


class PetSex(models.TextChoices):
    MALE = "male"
    FEMALE = "female"
    NOT_INFORMED = "not informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = PetSex.choices,
    default = PetSex.NOT_INFORMED
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="pets"
    )
