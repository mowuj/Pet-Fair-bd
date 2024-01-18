from django.urls import path
from .views import AddPetView, PetDetailView, AllPetView
urlpatterns = [
    path('all_pets/', AllPetView.as_view(), name="all_pets"),
    path('all_pets/<slug:category_slug>/',
         AllPetView.as_view(), name='category'),
    path('add_pet/',AddPetView.as_view(),name="add_pet"),
    path('pet_detail/<int:id>', PetDetailView.as_view(), name="pet_detail"),
]
