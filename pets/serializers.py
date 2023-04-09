from rest_framework import serializers

from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer

class PetSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField()
    group = GroupSerializer()
    traits = TraitSerializer(many=True)