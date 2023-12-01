from django.db import models


class Trait(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    pets = models.ManyToManyField(
        "pets.Pet",
        related_name="traits"
    )

    def __repr__(self) -> str:
        return f"<[{self.name}]>"
