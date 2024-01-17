from django.db import models
from django.contrib.auth.models import User
from . constants import RATING
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50,unique=True)

    def __str__(self):
        return self.name

class Pet(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    category=models.ManyToManyField(Category,related_name='pets')
    price = models.DecimalField(decimal_places=2,max_digits=12,default=0)
    image = models.ImageField(upload_to='pet/images',null=True,blank=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    user = models.ForeignKey(
        User, related_name="reviews", on_delete=models.CASCADE)
    pet = models.ForeignKey(
        Pet, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING)
    body = models.TextField()   
    models.DateTimeField(auto_now_add=True)
    timestamps = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
