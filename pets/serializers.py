from rest_framework import serializers
from .models import Sex
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer

class SexSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=Sex.choices, default = Sex.OTHER
    )
    
class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length = 50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=Sex.choices, default = Sex.OTHER
    )
    group = GroupSerializer()
    traits = TraitSerializer(many = True)
    