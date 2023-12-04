from rest_framework.views import APIView, status, Response, Request

from pets.models import Pet
from .serializers import PetSerializer

from traits.models import Trait
from groups.models import Group

# import ipdb

from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):

    def get(self, request: Request) -> Response:
        by_trait = request.query_params.get("trait_name", None)
        if by_trait:
            # pets = Pet.objects.filter(trait_name__icontains=by_trait)
            pets = Pet.objects.filter(traits__name__icontains=by_trait)
        else:
            pets = Pet.objects.all()
        result = self.paginate_queryset(pets, request)
        serializer = PetSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        groups_data = serializer.validated_data.pop("group")
        try:
            group = Group.objects.get(scientific_name=groups_data["scientific_name"])
        except Group.DoesNotExist:
            group = Group.objects.create(**groups_data)

        pet = Pet.objects.create(**serializer.validated_data, group=group)

        # traits
        traits_data = serializer.validated_data.pop("traits")


        for current_trait in traits_data:
            try:
                trait = Trait.objects.get(
                    name__iexact=current_trait["name"]
                )
            except Trait.DoesNotExist:
                trait = Trait.objects.create(**current_trait)
            pet.traits.add(trait)

        # pet.traits.set(traits)
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PetDetailView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        error_message = "Not found"
        try:
            found_pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response(
                {"detail": error_message},
                status.HTTP_404_NOT_FOUND
            )

        serializer = PetSerializer(found_pet)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, pet_id: int) -> Response:
        error_message = "Not found"
        try:
            remove_pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response(
                {"detail": error_message},
                status.HTTP_404_NOT_FOUND
            )

        remove_pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
