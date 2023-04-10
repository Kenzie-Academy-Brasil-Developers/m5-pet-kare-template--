from django.urls import path
from .views import Petview

urlpatterns = [
    path("pets/", Petview.as_view()),
]
