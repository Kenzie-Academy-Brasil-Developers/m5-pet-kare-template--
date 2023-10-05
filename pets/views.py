from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from .serializers import PetSerializer
from .models import Pet
from groups.models import Group
from traits.models import Trait


class PetView(APIView, PageNumberPagination):
    def post(self, req: Request) -> Response:
        serializer = PetSerializer(data=req.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        pet_data = serializer.validated_data
        traits: dict = pet_data.pop("traits")
        group: dict = pet_data.pop("group")

        try:
            found_group = Group.objects.get(
                scientific_name=group["scientific_name"]
            )
            group = found_group
        except Group.DoesNotExist:
            group = Group.objects.create(**group)

        pet = Pet.objects.create(**serializer.validated_data, group=group)

        traits_list = []
        for trait_data in traits:
            try:
                found_trait = Trait.objects.get(
                    name__iexact=trait_data["name"]
                )
                traits_list.append(found_trait)
            except Trait.DoesNotExist:
                trait = Trait.objects.create(**trait_data)
                traits_list.append(trait)

        pet.traits.set(
            traits_list
        )

        serializer = PetSerializer(pet)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, req: Request) -> Response:
        trait = req.query_params.get("trait", None)
        if trait is not None:
            pets = Pet.objects.filter(traits__name=trait)
        else:
            pets = Pet.objects.all()
        result = self.paginate_queryset(pets, req)
        serializer = PetSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class PetDetailedView(APIView):
    def get(self, req: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(pk=pet_id)
            serializer = PetSerializer(pet)
            return Response(serializer.data, status.HTTP_200_OK)
        except Pet.DoesNotExist:
            return Response(
                {"detail": "Not found."}, status.HTTP_404_NOT_FOUND
            )

    def delete(self, req: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(pk=pet_id)
            pet.delete()
            return Response(None, status.HTTP_204_NO_CONTENT)
        except Pet.DoesNotExist:
            return Response(
                {"detail": "Not found."}, status.HTTP_404_NOT_FOUND
            )

    def patch(self, req: Request, pet_id: int) -> Response:
        try:
            found_pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response(
                {"detail": "Not found."}, status.HTTP_404_NOT_FOUND
            )

        serializer = PetSerializer(data=req.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        pet_data = serializer.validated_data

        for key, value in pet_data.items():
            if key != "traits" and key != "group":
                setattr(found_pet, key, value)

        if pet_data.get("group") is not None:
            group: dict = pet_data.pop("group")
            try:
                found_group = Group.objects.get(
                    scientific_name=group["scientific_name"]
                )
                group = found_group
            except Group.DoesNotExist:
                group = Group.objects.create(**group)
            found_pet.group = group

        if pet_data.get("traits") is not None:
            traits: dict = pet_data.pop("traits")
            traits_list = []
            for trait_data in traits:
                try:
                    found_trait = Trait.objects.get(
                        name__iexact=trait_data["name"]
                    )
                    traits_list.append(found_trait)
                except Trait.DoesNotExist:
                    trait = Trait.objects.create(**trait_data)
                    traits_list.append(trait)

            found_pet.traits.set(
                traits_list
            )

        found_pet.save()
        serializer = PetSerializer(found_pet)

        return Response(serializer.data, status.HTTP_200_OK)
