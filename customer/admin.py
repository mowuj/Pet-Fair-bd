from django.contrib import admin
from .models import Customer,Contact
# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'content']
admin.site.register(Customer)
admin.site.register(Contact,ContactAdmin)