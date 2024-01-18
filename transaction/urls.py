from django.urls import path
from .views import DepositView,BuyPetView
urlpatterns = [
    path('deposit', DepositView.as_view(), name='deposit'),
    path('buy_pet/<int:id>/', BuyPetView.as_view(), name='buy_pet'),
]
