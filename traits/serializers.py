from rest_framework import serializers


class TraitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = models.CharField(max_length=20, unique=True)
    created_at = serializers.DateTimeField(read_only=True)