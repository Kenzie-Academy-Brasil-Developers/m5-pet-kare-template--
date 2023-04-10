from rest_framework import serializers
from .models import PetChoices
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=PetChoices.choices, 
                                  default=PetChoices.Not_Informed)

    traits = TraitSerializer(many=True)
    group = GroupSerializer()
