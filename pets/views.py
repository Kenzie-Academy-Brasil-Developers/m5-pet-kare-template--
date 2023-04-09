from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView, Response, Request
from rest_framework.pagination import PageNumberPagination
from pets.models import Pet
from traits.models import Trait
from groups.models import Group
from pets.serializers import PetSerializer
import ipdb


class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        query_param = request.query_params.get("trait", None)

        if query_param:
            pets = Pet.objects.filter(traits__name__iexact=query_param)
            result_page = self.paginate_queryset(pets, request, self)
            serializer = PetSerializer(result_page, many=True)
            return self.get_paginated_response(serializer.data)

        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request, self)
        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        trait_data = serializer.validated_data.pop("traits")
        group_data = serializer.validated_data.pop("group")

        group_dict = Group.objects.filter(
            scientific_name__iexact=group_data["scientific_name"]
        ).first()

        pet_instance_dict = Pet(**serializer.validated_data)

        if not group_dict:
            group_dict = Group(**group_data)
            group_dict.save()
            pet_instance_dict.group = group_dict

        pet_instance_dict.group = group_dict

        pet_instance_dict.save()

        for trait_dict in trait_data:
            trait_obj = Trait.objects.filter(name__iexact=trait_dict["name"]).first()

            if not trait_obj:
                trait_obj = Trait.objects.create(**trait_dict)

            pet_instance_dict.traits.add(trait_obj)

        serializer = PetSerializer(pet_instance_dict)

        return Response(serializer.data, 201)


class PetDetailView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)

        return Response(serializer.data, 200)

    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)
        trait_data = serializer.validated_data.pop("traits", None)

        if group_data:
            group_obj = Group.objects.filter(
                scientific_name=group_data["scientific_name"]
            ).first()
            if group_obj is None:
                new_group = Group(**group_data)
                new_group.save()
                pet.group = new_group
                pet.group.save()
            else:
                if group_data["scientific_name"] == group_obj.scientific_name:
                    pet.group = group_obj
                    pet.group.save()

        if trait_data:
            pet.traits.clear()
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
        serializer = PetSerializer(pet)

        return Response(serializer.data, 200)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)

        pet.delete()

        return Response(status=204)
