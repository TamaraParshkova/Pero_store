from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart

from catalog.models import Product
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart(request)
                    #cart_items = Cart.objects.filter(user=user)

                    if cart_items:
                        # Создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        # Создать заказанные товары
                        for cart_item in cart_items:
                            product=cart_item['product'],
                            price=cart_item['price'],
                            quantity=cart_item['quantity']    

                            if product[0].stock < quantity:
                                raise ValidationError(f'Недостаточное количество товара {product[0]} на складе. В наличии - {product[0].stock}')

                            cart_item = OrderItem.objects.create(
                                order=order,
                                product=product[0],
                                name = product[0],
                                price=price[0],
                                quantity=quantity,
                            )
                            print(cart_item)

                            product[0].stock -= quantity
                            product[0].save() 

                            print(product[0].stock)
                        # Очистить корзину пользователя после создания заказа
                        cart_items.clear()
                        messages.success(request, f"ВАШ ЗАКАЗ №{order.id} УСПЕШНО ОФОРМЛЕН. Наш менеджер свяжется с Вами для уточнения деталий доставки и оплаты.")
                        return redirect('home')
            except ValidationError as e:
                messages.error(request, str(*e))
                return redirect('order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'orders': True,
    }
    return render(request, 'orders/create_orders.html', context=context)