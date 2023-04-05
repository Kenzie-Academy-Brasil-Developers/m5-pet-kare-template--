from rest_framework import serializers
from models import SexOptions
from groups.serlializers import GroupsSerializer
from traits.serializers import TraitsSerializer

class PetsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=SexOptions.choices, default=SexOptions.DEFAULT)

    group = GroupsSerializer()
    traits = TraitsSerializer(many=True)