from django.db import models


class GenderChoices(models.TextChoices):
    Male = "Male"
    Female = "Female"
    Default = "Not Informed"
class Pet(models.Model):
  
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=20, choices=GenderChoices.choices, default=GenderChoices.Default)

    group = models.ForeignKey("groups.Group", on_delete=models.PROTECT, related_name="pets")