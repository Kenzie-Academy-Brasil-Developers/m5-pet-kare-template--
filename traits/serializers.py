from rest_framework import serializers


class TraitSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    created_at = serializers.DateTimeField()
    
 