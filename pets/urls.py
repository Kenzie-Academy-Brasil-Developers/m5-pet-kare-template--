from django.urls import path
from .views import PetView, PetDetailView

urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/<int:pet_id>/", PetDetailView.as_view()),
    # path("pets/<str:pet_trait>", PetDetailViewGetParams.as_view())
]
