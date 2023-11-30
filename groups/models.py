from django.db import models
from django.utils import timezone


# Create your models here.
class group(models.Model):
    """class group(models.Model):"""

    scientific_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
