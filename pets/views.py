from rest_framework.views import APIView, Request, Response, status
from .models import Pet
import ipdb
from .serializers import PetSerializer


class Petview(APIView):
    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()
        serializer = PetSerializer(instance=pets, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        pets = Pet.objects.create(**serializer.validated_data)

        serializer = PetSerializer(instance=pets)

        # serializer.data é igual ao model_to_dict(pets)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
