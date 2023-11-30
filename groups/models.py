from django.db import models
from django.utils import timezone


# Create your models here.
class group(models.Model):
    """class group(models.Model):
    representação dos grupos de pets.

    Atributos:
        scientific_name: Varchar(50) unique
        created_at: DateTimeField auto_now_add
            - Data de quando o grupo foi criado.

    Relacionamentos:
        - pet: any to many

    """

    scientific_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
