from django.urls import path
from pets.views import PetView, PetDetailView

urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/<int:id>/", PetDetailView.as_view()),
]
