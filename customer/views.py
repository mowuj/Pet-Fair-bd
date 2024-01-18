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
        return reverse_lazy('login')


class UserProfileView(LoginRequiredMixin, View):
    template_name = "customer/profile.html"

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        customer = self.request.user.customer
        buy = Transaction.objects.filter(
            transaction_type=BUY, customer=self.request.user.customer)
        total_buy_price = buy.aggregate(
            total_price=Sum('amount')
        )['total_price'] or 0

        return render(request, self.template_name, {"form": form, "buy": buy, "total_borrowing_price": total_buy_price, 'customer': customer})
