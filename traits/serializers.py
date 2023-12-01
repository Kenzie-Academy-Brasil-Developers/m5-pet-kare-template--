from rest_framework import serializers
from pets.serializers import PetSerializer


class TraitSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    trait_name = serializers.CharField(max_length=20, source="name")
    created_at = serializers.DateTimeField(read_only=True)
    pets = PetSerializer(many=True)
