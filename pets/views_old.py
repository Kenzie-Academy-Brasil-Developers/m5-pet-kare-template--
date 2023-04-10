# from django.shortcuts import render
# from django.forms.models import model_to_dict
# from rest_framework.views import APIView, Request, Response, status
# from .serializers import PetSerializer
# from .models import Pet
# from groups.serializers import GroupSerializer
# from traits.models import Trait


# class PetView(APIView):
#     def get(self, request: Request) -> Response: 
        
#         # Dado tipo QuerySet
#         pets = Pet.objects.all()
#         pet_list = []
#         traits = Trait.objects.all()

#         for pet in pets:
#             pet_dict = model_to_dict(pet)
            
#             pet_dict["group"] = [
#                 model_to_dict(group) 
#                 for group in pet.group.all()
                
#                 ]
            
#             # pet_dict["traits"] = [
#             #     model_to_dict(trait) for trait in pet in pet.traits.all()
#             # ]
            
#             pet_list.append(pet_dict)
#         # from groups.serializers import GroupSerializer

#         #     pet_dict["traits"] = [
#         #         model_to_dict(trait) for trait in pet in pet.traits.all()
#         #     ]

#         # serializer = PetSerializer(data=request.data)

#         return Response(pet_list, status.HTTP_200_OK)

#     def post(self, request: Request) -> Response:
#         pet = Pet.objects.create(**request.data)
#         pet_dict = model_to_dict(pet)
       
#         return Response(pet_dict, status.HTTP_201_CREATED)
    

#     from django.shortcuts import render
# from django.forms.models import model_to_dict
# from rest_framework.views import APIView, Request, Response, status
# from .serializers import PetSerializer
# from .models import Pet
# from groups.serializers import GroupSerializer
# from traits.models import Trait


# class PetView(APIView):
#     def get(self, request: Request) -> Response: 
        
#         # Dado tipo QuerySet
#         pets = Pet.objects.all()
#         pet_list = []
#         traits = Trait.objects.all()

#         for pet in pets:
#             pet_dict = model_to_dict(pet)
                        
#             pet_dict["group"] = [
#                 model_to_dict(group) 
#                 for group in pet.group.all()
                
#                 ]    
            
#             pet_dict["traits"] = [
#                 model_to_dict(traits) 
#                 for traits in pet.traits.all()
                
#                 ]
            
#             pet_list.append(pet_dict)
       
#         return Response(pet_list, status.HTTP_200_OK)

#     def post(self, request: Request) -> Response:
#         # pet = Pet.objects.create(**request.data)
#         # pet_dict = model_to_dict(pet)
#         return Response({"msg": "POOOST"})
#         # return Response(pet_dict, status.HTTP_201_CREATED)