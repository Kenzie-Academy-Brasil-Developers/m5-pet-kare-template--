from django.db import models


class Traits(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
