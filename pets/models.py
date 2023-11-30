from django.db import models


# Enum
class SexField(models.TextChoices):
    """class SexField(models.TextChoices):
    Enum TextChoices for Pet's sex
    MALE, FEMALE, NOT_INFORMED
    """

    MALE = "Male"
    FEMALE = "Female"
    NOT_INFORMED = "Not Informed"


# Create your models here.
class Pet(models.model):
    """class Pet(models.model):
    representação de um pet no petshop.

    Atributos:
        - name: varchar(50)
        - age: integer
        - weigth: float

    Relacionamentos:
        - group: any to many
        - traits: Many to Many

    """

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, choices=SexField.choices, default=SexField.NOT_INFORMED
    )

    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, related_name="pets"
    )
