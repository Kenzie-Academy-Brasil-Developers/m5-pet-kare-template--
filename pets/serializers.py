from rest_framework import serializers
from .models import PetChoices
from traits.serializers import TraitSerializer


class PetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=PetChoices.choices, 
                                  default=PetChoices.Not_Informed)
    traits = TraitSerializer(many=True, read_only=True)