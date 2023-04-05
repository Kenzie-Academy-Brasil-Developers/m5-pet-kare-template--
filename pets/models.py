from django.db import models

class Sex(models.TextChoices):
    MALE = "Male",
    FEMALE = "Female",
    DEFAULT = "Not Informed"

class Pet(models.Model):
    name = models.CharField(max_length = 50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length = 20, choices = Sex.choices, default = Sex.DEFAULT)

    group = models.ForeignKey(
        "groups.Group",
        on_delete = models.PROTECT,
        related_name = "pets"
    )

    traits = models.ManyToManyField(
        "traits.Trait",
        related_name="pet"
    )

    def __repr__(self) -> str:
        return f"<Pet ({self.id} - {self.name} - {self.group} - {self.traits})>"

# Create your models here.
