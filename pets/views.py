from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from rest_framework.pagination import PageNumberPagination
from pets.models import Pet
from groups.models import Group
from traits.models import Trait
from pets.serializers import PetSerializer
from django.shortcuts import get_object_or_404

class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        traits = request.query_params.get("trait", None)
        if traits:
            pets = Pet.objects.filter(traits__name=traits).all()
        else:
            pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request)
        serializer = PetSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)
    
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_data = serializer.validated_data.pop("group")
        traits_data = serializer.validated_data.pop("traits")
        pet_obj = Pet.objects.create(**serializer.validated_data)

        for traits in traits_data:
            traits_obj = Trait.objects.filter(name__iexact=traits["name"].lower()).first()
            if not traits_obj:
                traits_obj = Trait.objects.create(**traits)
            pet_obj.traits.add(traits_obj)

        group_obj = Group.objects.filter(scientific_name__iexact=group_data["scientific_name"].lower()).first()
        if not group_obj:
            group_obj = Group.objects.create(**group_data)
        pet_obj.group = group_obj

        serializer = PetSerializer(instance=pet_obj)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class PetIdView(APIView):
    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        group_data = serializer.validated_data.pop("group", None)
        traits_data = serializer.validated_data.pop("traits", None)

        if traits_data:
            for traits in traits_data:
                traits_obj = Trait.objects.filter(name__iexact=traits["name"].lower()).first()
                if not traits_obj:
                    traits_obj = Trait.objects.create(**traits)
                pet.traits.add(traits_obj)

        if group_data:
            group_obj = Group.objects.filter(scientific_name__iexact=group_data["scientific_name"].lower()).first()
            if not group_obj:
                group_obj = Group.objects.create(**group_data)
            pet.group = group_obj

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Create your views here.
