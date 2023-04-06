from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from rest_framework.pagination import PageNumberPagination
from pets.models import Pet
from groups.models import Group
from traits.models import Trait
from pets.serializers import PetSerializer

class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
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
    print("olá")

# Create your views here.
