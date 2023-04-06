from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=20, choices=(("Male", "Male"), ("Female", "Female"), ("Not Informed", "Not Informed")), default="Not Informed")

    group = models.OneToOneField("groups.Group", on_delete=models.PROTECT)