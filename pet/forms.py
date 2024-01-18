from django import forms
from .models import Pet,Review
from .constants import RATING
class PetForm(forms.ModelForm):
    class Meta:
        model=Pet
        exclude=['user']
    

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=RATING)
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Review
        fields = ['rating','body']
