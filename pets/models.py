from django.db import models


class SexOptions(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    NOT_INFORMED = "Not informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, choices=SexOptions.choices, default=SexOptions.NOT_INFORMED
    )

    group = models.ForeignKey(
        "groups.Group", related_name="pets", on_delete=models.RESTRICT
    )
    traits = models.ManyToManyField("traits.Trait", related_name="pets", null=True)
