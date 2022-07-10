from django.contrib import admin

from copy_trade.models import Order, Stage, Basket

# Register your models here.
admin.site.register(Stage)
admin.site.register(Basket)
admin.site.register(Order)