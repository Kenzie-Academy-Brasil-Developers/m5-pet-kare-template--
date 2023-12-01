from rest_framework import serializers
from groups.serializers import GroupSerializer

from pets.models import SexField


class PetSerializer(serializers.Serializer):
    """class PetSerializer(serializers.Serializer):"""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_lenght=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField(
        max_lenght=20, choices=SexField.choices, default=SexField.NOT_INFORMED
    )

    group = GroupSerializer()

    traits = ...
