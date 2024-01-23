from django.shortcuts import render,redirect
from pet.models import Pet
from customer.models import Contact
from customer.forms import ContactForm
from django.views.generic import CreateView
from django.views import View
from django.urls import reverse_lazy


class HomeView(View):
    template_name='home.html'

    def get(self,request):
        data = Pet.objects.all()
        contact_form=ContactForm()
        return render(request,self.template_name,{'form':contact_form,'data':data})
    
    def post(self,request):
        data = Pet.objects.all()
        contact_form=ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect('home')
        return render(request, self.template_name,{'data': data,'form':contact_form})