from django import forms
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.forms import UserCreationForm
from .constants import GENDER


class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=12)
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect)
    street_address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    image=forms.ImageField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name',
                  'last_name', 'email', 'gender', 'street_address', 'city', 'country', 'image']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            phone = self.cleaned_data.get('phone')
            gender = self.cleaned_data.get('gender')
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            country = self.cleaned_data.get('country')
            image = self.cleaned_data.get('image')

            Customer.objects.create(
                user=user,
                customer_id=10000+user.id,
                phone=phone,
                gender=gender,
                street_address=street_address,
                city=city,
                country=country,
                image=image
            )
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UserUpdateForm(forms.ModelForm):
    phone = forms.CharField(max_length=12)
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect)
    street_address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    image = forms.ImageField()

    class Meta:
        model=User
        fields = ["first_name", "last_name"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            try:
                customer = self.instance.customer
            except:
                customer = None

            if customer:
                self.fields['phone'].initial = customer.phone
                self.fields['gender'].initial = customer.gender
                self.fields['street_address'].initial = customer.street_address
                self.fields['city'].initial = customer.city
                self.fields['country'].initial = customer.country
                self.fields['image'].initial = customer.image

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            customer, created = Customer.objects.get_or_create(user=user)

            customer.phone = self.cleaned_data.get("phone")
            customer.gender = self.cleaned_data.get("gender")
            customer.street_address = self.cleaned_data.get("street_address")
            customer.city = self.cleaned_data.get("city")
            customer.country = self.cleaned_data.get("country")
            customer.image = self.cleaned_data.get("image")
            customer.save()

        return user
