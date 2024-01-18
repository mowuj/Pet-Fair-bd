from django.contrib import admin
from . models import Transaction
# Register your models here.


class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ['customer_name','pet',
                    'amount', 'transaction_type', 'timestamps']

    def customer_name(self, obj):
        return obj.customer.user.username

admin.site.register(Transaction, TransactionModelAdmin)
