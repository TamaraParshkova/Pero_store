from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponse
from cart.forms import CartAddProductForm
from .models import *

def products(request):
    cart_product_form = CartAddProductForm()
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    return render(request, 'catalog/catalog.html', locals())

def show_prod(request, prod_slug):
    cart_product_form = CartAddProductForm()
    prod = Product.objects.get(slug=prod_slug)
    return render(request, 'catalog/show_prod.html', locals())

