from django.urls import path
from .views import AddPetView, PetDetailView, AllPetView, PetEditView, PetDeleteView
urlpatterns = [
    path('all_pets/', AllPetView.as_view(), name="all_pets"),
    path('all_pets/<slug:category_slug>/',
         AllPetView.as_view(), name='category'),
    path('add_pet/',AddPetView.as_view(),name="add_pet"),
    path('edit_pet/<int:id>', PetEditView.as_view(), name="edit_pet"),
    path('pet_detail/<int:id>', PetDetailView.as_view(), name="pet_detail"),
    path('pet_delete/<int:id>', PetDeleteView.as_view(), name="pet_delete"),
]
