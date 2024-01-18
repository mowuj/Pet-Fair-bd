from django.shortcuts import render
from pet.models import Pet
def home(request):
    data = Pet.objects.all()

    return render(request, 'home.html', {'data': data})