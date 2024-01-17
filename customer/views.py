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


class UserRegistrationView(FormView):
    template_name=''
    success_url=reverse_lazy('')
    form_class=UserRegistrationForm

    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        messages.success(self.request,"Welcome! You have registered Successfully")
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name=''

    def get_success_url(self):
        messages.success(self.request, "You are Successfully logged in ")
        return reverse_lazy('profile')
