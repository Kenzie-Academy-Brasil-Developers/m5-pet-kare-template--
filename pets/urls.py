from django.urls import path
from . import views

urlpatterns = [
    path('pets/',
         views.PetView.as_view()
         ),
]

