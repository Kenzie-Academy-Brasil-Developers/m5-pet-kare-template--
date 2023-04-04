from rest_framework import serializers


class GroupSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    scientific_name = serializers.CharField(max_length=50, unique=True)
    created_at = serializers.DateTimeField(read_only=True)
