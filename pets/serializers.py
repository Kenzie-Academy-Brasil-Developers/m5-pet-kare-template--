from rest_framework import serializers

from groups.serializers import GroupSerializer
from traits.serializers import TraitsSerializer
from .models import PetSex


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=PetSex.choices,
        default=PetSex.DEFAULT,
    )

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    group = GroupSerializer(
        read_only=True,
    )
    traits = TraitsSerializer(many=True, read_only=True)
