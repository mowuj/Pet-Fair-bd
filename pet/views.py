from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .models import Pet,Category
from .forms import PetForm
from django.views.generic import CreateView,UpdateView,DetailView,DeleteView
# Create your views here.

class AddPetView(CreateView):
    model=Pet
    form_class = PetForm
    template_name='pet/add_pet.html'
    success_url=reverse_lazy('add_pet')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    

class PetDetailView(DetailView):
    model = Pet
    pk_url_kwarg='id'
    template_name='pet/pet_detail.html'