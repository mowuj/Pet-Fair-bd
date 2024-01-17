from django.contrib import admin
from . models import Transaction
# Register your models here.


class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ['customer',
                    'amount', 'transaction_type', 'timestamps']

    def customer(self, obj):
        return obj.customer.user.first

admin.site.register(Transaction, TransactionModelAdmin)
