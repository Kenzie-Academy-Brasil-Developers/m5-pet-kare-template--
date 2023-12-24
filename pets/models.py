from django.db import models

class Sex(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Not Informed"
    
class Pet(models.Model):
    name = models.CharField(max_length = 50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length = 20, choices = Sex.choices ,default = Sex.OTHER )
    group = models.ForeignKey(
        "groups.Group",
        on_delete = models.PROTECT,
        null = True,
        related_name = "pets"
    )
    traits = models.ManyToManyField("traits.Trait", related_name="trait")