from django.urls import path
from .views import PetsView, PetDetailView

urlpatterns = [
    path("pets/", PetsView.as_view()), 
    path("pets/<int:pet_id>/", PetDetailView.as_view()) 
    ]