from django.urls import path
from .views import AddPetView,PetDetailView
urlpatterns = [
    path('add_pet/',AddPetView.as_view(),name="add_pet"),
    path('pet_detail/', PetDetailView.as_view(), name="pet_detail"),
]
