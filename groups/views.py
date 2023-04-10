from django.shortcuts import render
from django.dispatch import receiver
from rest_framework.views import APIView, Request, Response, status
from groups.models import Group
from groups.serializers import GroupSerializer
from pets.models import Pet
from rest_framework.pagination import PageNumberPagination

...
            