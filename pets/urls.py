from django.urls import path
from pets.views import PetView

urlpatterns = [
    path("pets/", PetView.as_view()),
]
