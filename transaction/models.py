from django.db import models
from .constants import TRANSACTION_TYPE
from customer .models import Customer
from pet .models import Pet
# Create your models here.


class Transaction(models.Model):
    customer = models.ForeignKey(
        Customer, related_name='transaction', on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, related_name='buy_pet',
                             on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(
        decimal_places=2, max_digits=12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE)
    timestamps = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.customer.user.username)
