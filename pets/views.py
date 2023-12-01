from rest_framework.views import APIView, status, Response, Request

from pets.models import Pet
from .serializers import PetSerializer

from traits.models import Trait
from groups.models import Group

import ipdb

from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        ipdb.set_trace()
        pet = Pet.objects.create(**serializer.validated_data)
        # group
        groups_data = serializer.validated_data.pop("group")

        for current_group in groups_data:
            try:
                group = Group.objects.get(current_group["group"])
                group.pets.add(pet)
            except Group.DoesNotExist:
                group = Group.objects.create(**current_group)
                group.pets.add(pet)
        # traits
        traits_data = serializer.validated_data.pop("traits")

        # traits = []

        for current_trait in traits_data:
            #     trait = Trait.objects.create(**current_trait)
            #     traits.append(trait)
            try:
                trait = Trait.objects.get(
                    name__iexact=current_trait["trait_name"]
                )
                trait.pets.add(pet)
            except Trait.DoesNotExist:
                trait = Trait.objects.create(**current_trait)
                trait.pets.add(pet)

        # pet.traits.set(traits)
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request):
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)
