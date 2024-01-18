from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout, update_session_auth_hash
from django.db.models import Sum
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from transaction.models import Transaction
from transaction.constants import BUY
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .models import Customer
from django.contrib.auth.models import User
from pet .models import Pet
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class UserRegistrationView(FormView):
    template_name = 'customer/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user = form.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f"http://127.0.0.1:8000/customer/active/{uid}/{token}"
        email_subject="Confirm Your Email"
        email_body=render_to_string('customer/confirm_mail.html',{'confirm_link':confirm_link})
        email=EmailMultiAlternatives(email_subject,'',to=[user.email])
        email.attach_alternative(email_body,"text/html")
        email.send()

        messages.success(
            self.request, "Welcome! You have registered Successfully. Check your email to confirm your account."
        )

        login(self.request, user)

        return super().form_valid(form)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=int(uid))
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('profile')
    else:
        return redirect('login')
    
class UserLoginView(LoginView):
    template_name='customer/login.html'

    def get_success_url(self):
        messages.success(self.request, "You are Successfully logged in ")
        return reverse_lazy('profile')


@method_decorator(login_required, name='dispatch')
class UserProfileView(LoginRequiredMixin, View):
    template_name = "customer/profile.html"

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        pets=Pet.objects.filter(user=request.user)
        customer = self.request.user.customer
        transaction = Transaction.objects.filter(customer=self.request.user.customer)
        total = transaction.aggregate(
            total_price=Sum('amount')
        )['total_price'] or 0
        buy = Transaction.objects.filter(
            transaction_type=BUY, customer=self.request.user.customer)
        total_buy_price = buy.aggregate(
            total_price=Sum('amount')
        )['total_price'] or 0

        return render(request, self.template_name, {"form": form, "buy": buy, "total_buy_price": total_buy_price, 'customer': customer, "pets": pets, "transaction": transaction,"total":total})


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'customer/edit_profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


@login_required
def change_pass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed Successfully')
            update_session_auth_hash(request, form.user)

            mail_subject = 'Password Change'
            message = render_to_string('customer/pass_change_mail.html', {
                'user': request.user
            })
            to_email = request.user.email
            send_email = EmailMultiAlternatives(
                mail_subject, '', to=[to_email])
            send_email.attach_alternative(message, "text/html")
            send_email.send()
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'customer/change_pass.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('login')
