from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from .models import Transaction
from .forms import DepositForm, BuyPetForm
from .constants import DEPOSIT, BUY
from django.contrib import messages
from django.urls import reverse_lazy
from pet.models import Pet
from django.db.models import Sum
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.


def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

class TransactionViewMixin(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'transaction/transaction.html'
    success_url = reverse_lazy('profile')
    title = ''

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'customer': self.request.user.customer
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context


class DepositView(TransactionViewMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        customer = self.request.user.customer
        customer.balance += amount
        customer.save(
            update_fields=['balance']
        )
        messages.success(self.request,
                         f'{"{:,.2f}".format(float(amount))}$ has ben successfully Deposit')
        send_transaction_email(
            self.request.user, amount, 'Deposit Message', 'transaction/deposit_email.html')
        
        return super().form_valid(form)


class BuyPetView(TransactionViewMixin):
    form_class = BuyPetForm
    title = 'Buy Pet'

    def get_initial(self):
        id = self.kwargs['id']
        pet = Pet.objects.get(pk=id)
        initial = {'transaction_type':BUY,
                   'amount': pet.price, 'pet': pet}
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        pet = Pet.objects.get(id=id)
        context.update({
            'pet': pet
        })
        return context

    def form_valid(self, form):
        id = self.kwargs['id']
        customer = self.request.user.customer
        pet = Pet.objects.get(id=id)
        amount = pet.price

        if customer.balance < amount:
            messages.error(
                self.request, f'Opps ! You don not have enough Balance.Please Deposit')
            return redirect('profile')

        customer.balance -= amount
        customer.save(
            update_fields=['balance']
        )
        messages.success(self.request,
                         f'Welcome! You has ben successfully Buy this pet.Your current balance is ${customer.balance}')
        send_transaction_email(
            self.request.user, amount, 'Buy Message', 'transaction/buy_email.html')
        
        return super().form_valid(form)
