from django.shortcuts import render
from rest_framework.views import Request, Response, APIView,status
from .models import Pet
from .serializers import PetSerializer
from groups.models import Group
from traits.models import Trait
from rest_framework.pagination import PageNumberPagination

class PetsView(APIView, PageNumberPagination):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        group_data = serializer.validated_data.pop("group")
                
        trait_data = serializer.validated_data.pop("traits")

        existing_group = Group.objects.filter(scientific_name__iexact = group_data["scientific_name"]).first()

        if existing_group:
            pet = Pet.objects.create(**serializer.validated_data, group = existing_group)
        else:
            group = Group.objects.create(**group_data)
            pet = Pet.objects.create(**serializer.validated_data, group = group)

        
        for current_trait_data in trait_data:
            trait_name_lower = current_trait_data["name"].lower()
            existing_trait = Trait.objects.filter(name__iexact=trait_name_lower).exists()

            if existing_trait:
                trait = Trait.objects.get(name__iexact=trait_name_lower)
                pet.traits.add(trait)
            else:
                trait_data_without_name = {key: value for key, value in current_trait_data.items() if key != "name"}
                trait = Trait.objects.create(name=trait_name_lower, **trait_data_without_name)
                pet.traits.add(trait)

        serializer = PetSerializer(pet)


        return Response(serializer.data, status.HTTP_201_CREATED)

    
    def get(self, request):
        by_trait = request.query_params.get("trait",None)

        if by_trait:
            pets = Pet.objects.filter(traits__name__iexact = by_trait)
        else:
            pets = Pet.objects.all()

        result = self.paginate_queryset(pets, request)

        serializer = PetSerializer(result, many=True)

        return self.get_paginated_response(serializer.data)

class PetDetailView(APIView):
    def get(self, request:Request, pet_id:int) -> Response:
        try:
            found_pet = Pet.objects.get(id = pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_400_BAD_REQUEST)
        
        serializer = PetSerializer(found_pet)
        return Response(serializer.data, status.HTTP_200_OK)
        
    def delete(self, request:Request, pet_id:int) -> Response:
        try:
            found_pet = Pet.objects.get(id = pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
        
        found_pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
    def patch(self, request:Request, pet_id:int) -> Response:
        try:
            found_pet = Pet.objects.get(id = pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
        
        
        serializer = PetSerializer(data=request.data, partial = True)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        group_data = serializer.validated_data.pop("group", None)   
        
        trait_data = serializer.validated_data.pop("traits", None)     


        for key, value in serializer.validated_data.items():
            setattr(found_pet, key, value)

            found_pet.save()
        
        if group_data:
            found_pet.group.scientific_name = group_data["scientific_name"]
            found_pet.save()
                
            
        serializer = PetSerializer(found_pet)
        
        return Response(serializer.data, status.HTTP_200_OK)