from django.db import models
from django.utils import timezone


class Group(models.Model):
    scientific_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
