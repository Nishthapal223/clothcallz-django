from django.contrib import admin
from .models import Product, Cart, Address, Order

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Order)
