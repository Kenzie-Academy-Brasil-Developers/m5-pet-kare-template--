from rest_framework import serializers


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    scientific_name = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
