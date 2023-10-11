from django.db import models


# Create your models here.
class SexField(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    NOT_INFORMED = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=30, choices=SexField.choices, default=SexField.NOT_INFORMED
    )
    group = models.ForeignKey(
        "groups.group", on_delete=models.RESTRICT, related_name="groups"
    )

    trait = models.ManyToManyField("traits.Trait", related_name="traits")
