from django.shortcuts import render
from rest_framework.views import APIView, Response, Request, status
from rest_framework.pagination import PageNumberPagination
from .serializers import PetSerializer
from .models import Pet
from groups.models import Group
from traits.models import Trait
import ipdb
from django.shortcuts import get_object_or_404


class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        pet_trait = request.query_params.get("trait", None)

        pets = Pet.objects.filter(traits=pet_trait)

        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)
        PetSerializer()

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group")
        trait_data = serializer.validated_data.pop("traits")

        group_filter = Group.objects.filter(
            scientific_name__iexact=group_data["scientific_name"]
        ).first()
        if not group_filter:
            group_obj = Group.objects.create(**group_data)
        else:
            group_obj = group_filter

        pet_obj = Pet.objects.create(**serializer.validated_data, group=group_obj)

        for trait_dict in trait_data:
            trait_obj = Trait.objects.filter(name__iexact=trait_dict["name"]).first()

            if not trait_obj:
                trait_obj = Trait.objects.create(**trait_dict)

            pet_obj.traits.add(trait_obj)

        serializer = PetSerializer(instance=pet_obj)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class PetDetailView(APIView):
    def get(self, request: Request, id) -> Response:
        pet = get_object_or_404(Pet, id=id)
        serializer = PetSerializer(pet)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, id) -> Response:
        pet = get_object_or_404(Pet, id=id)
        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)
        trait_data = serializer.validated_data.pop("traits", None)

        if group_data:
            group_filter = Group.objects.filter(
                scientific_name__iexact=group_data["scientific_name"]
            ).first()
            if not group_filter:
                Group.objects.create(**group_data)
        if trait_data:
            for trait_dict in trait_data:
                trait_obj = Trait.objects.filter(
                    name__iexact=trait_dict["name"]
                ).first()

                if not trait_obj:
                    trait_obj = Trait.objects.create(**trait_dict)

                pet.traits.add(trait_obj)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(instance=pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, id) -> Response:
        pet = get_object_or_404(Pet, id=id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
