from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from pet_kare.pagination import CustomPageNumberPagination
from pets.serializers import PetSerializer
from groups.serializers import GroupSerializer
from pets.models import Pet
from groups.models import Group
from traits.models import Trait

# Create your views here.


class PetView(APIView, CustomPageNumberPagination):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group")
        trait_data = serializer.validated_data.pop("traits")

        find_group = Group.objects.filter(
            scientific_name__iexact=group_data["scientific_name"]
        ).first()

        if not find_group:
            find_group = Group.objects.create(**group_data)

        pet = Pet.objects.create(**serializer.validated_data, group=find_group)

        trait_instances = []

        for trait in trait_data:
            find_trait = Trait.objects.filter(
                name__iexact=trait["name"]
            ).first()
            if not find_trait:
                find_trait = Trait.objects.create(**trait)
            trait_instances.append(find_trait)

        pet.traits.set(trait_instances)
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)
