from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.urls import reverse, reverse_lazy
from catalog.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# @login_required(redirect_field_name='home')
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = CartAddProductForm(request.POST)    
        if form.is_valid():  
            cd = form.cleaned_data
            if cd['quantity']<=product.stock:

                cart.add(product=product,
                        quantity=cd['quantity'],
                        update_quantity=cd['update'])
                messages.success(request, "Товар добавлен в карзину")
            else:
                messages.error(request, f'Недостаточное количество товара {product} на складе. В наличии - {product.stock}')            

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), locals())


def cart_decrease(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = 1  # Уменьшаем количество на 1
    if str(product_id) in cart.cart and cart.cart[str(product_id)]['quantity'] > 1:
        cart.decrease(product=product, quantity=quantity, update_quantity=False)
    elif str(product_id) in cart.cart and cart.cart[str(product_id)]['quantity'] == 1:
        cart.decrease(product=product, quantity=quantity, update_quantity=False)
        del cart.cart[str(product_id)]
        cart.save()
    return redirect('cart_detail')

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'), locals())
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart,'show_button': True})