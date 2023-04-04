from rest_framework import serializers
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer


sex_options = (
    ("Male"),
    ("Female"),
    ("Not Informed"),
)


class PetSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=sex_options, required=False)
    group = GroupSerializer(many=False)
    traits = TraitSerializer(many=True)
