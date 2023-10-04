from django.urls import path
from .views import PetView

urlpatterns = [
    path("pets/", PetView.as_view()),
]
