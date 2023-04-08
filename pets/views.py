from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import PetsSerializer
from groups.models import Group
from traits.models import Trait
from .models import Pet


class PetsView(APIView, PageNumberPagination):
    def post(self, request):
        serializer = PetsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_obj = serializer.validated_data.pop("group")
        traits = serializer.validated_data.pop("traits")

        group_in_db = Group.objects.filter(
            scientific_name__iexact=group_obj["scientific_name"]
        ).first()

        if not group_in_db:
            group_in_db = Group.objects.create(**group_obj)

        pet_obj = Pet.objects.create(**serializer.validated_data, group=group_in_db)

        for trait in traits:
            trait_data = Trait.objects.filter(name__iexact=trait["name"]).first()
            if not trait_data:
                trait_data = Trait.objects.create(**trait)
            pet_obj.traits.add(trait_data)

        serializer = PetsSerializer(pet_obj)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request):
        trait_params = request.query_params.get("trait", None)

        if trait_params is not None:
            pets = Pet.objects.filter(traits__name=trait_params)
        else:
            pets = Pet.objects.all()
            
        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetsSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)