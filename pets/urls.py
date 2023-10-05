from django.urls import path
from .views import PetView, PetDetailedView

urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/<int:pet_id>/", PetDetailedView.as_view()),
]
