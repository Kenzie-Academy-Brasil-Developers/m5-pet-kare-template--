from django.db import models
from django.utils import timezone


# Create your models here.
class Trait(models.Model):
    """class Trait(models.Model):

    Atributos:
       name: Varchar(50) unique
       created_at: DateTimeField auto_now_add
           - Data de quando o grupo foi criado.

    """

    name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
