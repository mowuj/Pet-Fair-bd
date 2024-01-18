from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .models import Pet,Category
from .forms import PetForm
from django.views.generic import CreateView,UpdateView,DetailView,DeleteView
from django.views import View
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


class AllPetView(View):
    template_name = 'pet/all_pets.html'

    def get(self, request, category_slug=None):
        data = Pet.objects.all()

        if category_slug is not None:
            category = Category.objects.get(slug=category_slug)
            data = Pet.objects.filter(category=category)

        categories = Category.objects.all()

        return render(request, self.template_name, {'data': data, 'category': categories})
