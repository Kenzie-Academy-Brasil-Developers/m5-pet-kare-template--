from rest_framework import serializers
from .models import PetSex
from groups.seriaizers import GroupSerializer
from traits.serializers import TraitSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=PetSex.choices,
        default=PetSex.not_informad,
    )
    group = GroupSerializer(many=False, read_only=True)
    traits = TraitSerializer(many=True, read_only=True)
