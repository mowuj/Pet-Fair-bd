from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .models import Pet,Category,Review
from .forms import PetForm,ReviewForm
from django.views.generic import CreateView,UpdateView,DetailView,DeleteView
from django.views import View
from django.contrib import messages
from transaction . models import Transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.


@method_decorator(login_required, name='dispatch')
class AddPetView(CreateView):
    model=Pet
    form_class = PetForm
    template_name='pet/add_pet.html'
    success_url=reverse_lazy('add_pet')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    

@method_decorator(login_required, name='dispatch')
class PetDetailView(DetailView):
    model = Pet
    pk_url_kwarg = 'id'
    template_name = 'pet/pet_detail.html'
    context_object_name = 'pet'

    def post(self, request, *args, **kwargs):
        pet = self.get_object()
        review_form = ReviewForm(data=request.POST)

        if review_form.is_valid():
            is_buy = Transaction.objects.filter(
                pet=pet, customer=self.request.user.customer).exists()
            if is_buy==False:
                messages.info(
                    request, "You can Review only after buy this pet.")
                return redirect("profile")
            is_already_reviewed = Review.objects.filter(
                pet=pet, user=request.user).exists()

            if is_already_reviewed:
                messages.info(request, "You have already reviewed for this pet.")
                return redirect('pet_detail', id=pet.id)

            new_review = review_form.save(commit=False)
            new_review.pet = pet
            new_review.user = request.user
            new_review.save()

            messages.success(request, "Thanks for your valuable review")

            return render(request, self.template_name, self.get_context_data())

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = self.get_object()
        review = pet.reviews.all()
        review_form = ReviewForm()

        context['review'] = review
        context['review_form'] = review_form
        return context


@method_decorator(login_required, name='dispatch')
class AllPetView(View):
    template_name = 'pet/all_pets.html'

    def get(self, request, category_slug=None):
        data = Pet.objects.all()

        if category_slug is not None:
            category = Category.objects.get(slug=category_slug)
            data = Pet.objects.filter(category=category)

        categories = Category.objects.all()

        return render(request, self.template_name, {'data': data, 'category': categories})


@method_decorator(login_required, name='dispatch')
class PetEditView(LoginRequiredMixin, View):
    template_name = 'pet/edit_pet.html'
    pk_url_kwarg = 'id'

    def get(self, request, id):
        pet_instance = get_object_or_404(Pet, id=id, user=request.user)
        form = PetForm(instance=pet_instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, id):
        pet_instance = get_object_or_404(Pet, id=id, user=request.user)
        form = PetForm(request.POST, instance=pet_instance)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = 'pet/delete_pet.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Pet.objects.filter(user=self.request.user)

