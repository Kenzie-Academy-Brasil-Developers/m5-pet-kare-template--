from rest_framework import serializers
from .models import PetSexOptions
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=PetSexOptions.choices, default=PetSexOptions.not_informed
    )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
