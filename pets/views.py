from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from rest_framework.views import APIView, Request, Response, status
from groups.models import Group

from traits.serializers import TraitSerializer
from .serializers import PetSerializer
from .models import Pet
from groups.serializers import GroupSerializer
from traits.models import Trait
from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response: 
        pets = Pet.objects.all()
        
        trait_name = request.query_params.get("trait")
        if trait_name:
            pets = pets.filter(traits__name__iexact=trait_name)

        result_page = self.paginate_queryset(pets, request)

        serializer = PetSerializer(result_page, many=True)
        
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        traits = serializer.validated_data.pop("traits")
        group = serializer.validated_data.pop("group")
    
        pet_obj = Pet.objects.create(**serializer.validated_data)

        group_obj, _ = Group.objects.get_or_create(**group)
        pet_obj.group = group_obj
        pet_obj.save()
 
        for trait_dict in traits: 
            trait_obj = Trait.objects.filter(
                name__iexact=trait_dict["name"]
            ).first()

            if not trait_obj:
                trait_obj = Trait.objects.create(**trait_dict)
                
            pet_obj.traits.add(trait_obj)

        serializer = PetSerializer(pet_obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PetDetailView(APIView, PageNumberPagination):
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

        if group_data:
            try:        
               
                group_obj, _ = Group.objects.get_or_create(**group_data)
                if pet.group and pet.group.id != group_obj.id:
                    pet.group.pets.remove(pet)
                pet.group = group_obj
                pet.save()
                    
            except Pet.group.RelatedObjectDoesNotExist:
                Group.objects.create(**group_data)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()

        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT) 
    
 
   