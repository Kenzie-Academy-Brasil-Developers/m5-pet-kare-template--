from django.shortcuts import render
from rest_framework.views import APIView, Response, Request
from rest_framework.pagination import PageNumberPagination
from pets.models import Pet
from traits.models import Trait
from groups.models import Group
from pets.serializers import PetSerializer


class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request, self)
        serializer = PetSerializer(result_page, many=True)
        return self.get_paginated_response(serializer)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        traits = serializer.validated_data.pop("traits")
        group = serializer.validated_data.pop("group")

        group_dict = Group.objects.filter(
            scientific_name__iexact=group["scientific_name"]
        ).first()

        pet_instance_dict = Pet(**serializer.validated_data)

        if not group_dict:
            group_dict = Group(**group)
            group_dict.save()
            pet_instance_dict.group = group_dict

        pet_instance_dict.group = group_dict

        pet_instance_dict.save()

        for trait_dict in traits:
            trait_obj = Trait.objects.filter(name__iexact=trait_dict["name"]).first()

            if not trait_obj:
                trait_obj = Trait.objects.create(**trait_dict)

            pet_instance_dict.traits.add(trait_obj)

        serializer = PetSerializer(pet_instance_dict)

        return Response(serializer.data, 201)
