from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class PetView(APIView, PageNumberPagination):
    def post(self, request: Request) -> Response:
        ...
