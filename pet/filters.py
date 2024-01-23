import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class PetFilter(django_filters.FilterSet):
    class Meta:
        model = Pet
        fields = '__all__'
        exclude=[
            'user',
            'category',
            'image',
            'availability',
        
        ]
