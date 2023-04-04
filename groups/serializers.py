from rest_framework import serializers


class GroupSerializer(serializers.Serializer):
    scientific_name = serializers.CharField(max_length=50)
    created_at = serializers.DateTimeField()