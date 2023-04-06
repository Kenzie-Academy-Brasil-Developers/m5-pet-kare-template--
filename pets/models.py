from django.db import models


class PetSex(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    DEFAULT = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, default=PetSex.DEFAULT, choices=PetSex.choices
    )

    traits = models.ManyToManyField("traits.Trait", related_name="pets")

    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, related_name="pets"
    )

    def __repr__(self) -> str:
        return f"<Pet ({self.id}) - {self.name}>"
