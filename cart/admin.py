from django.contrib import admin
from cart.cart import Cart

class CartTabAdmin(admin.TabularInline):
    model=Cart
