from django.contrib import admin

from transaction.models import DiscountCode, Transaction

# Register your models here.
admin.site.register(DiscountCode)
admin.site.register(Transaction)