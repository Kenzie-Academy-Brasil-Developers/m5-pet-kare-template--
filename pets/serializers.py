from rest_framework import serializers
from .models import Sex

class SexSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=Sex.choices, default = Sex.OTHER
    )