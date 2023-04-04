from django.db import models


class PetSex(models.TextChoices):
    name = "Male"
    female = "Female"
    not_informad = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, choices=PetSex.choices, default=PetSex.not_informad
    )
    group = models.ForeignKey(
        "groups.Group", on_delete=models.RESTRICT, related_name="Pets"
    )
    trait = models.ManyToManyField("traits.Trait", related_name="pets")
