from django.conf import settings
from catalog.models import Product
from decimal import Decimal

class Cart(object):
    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add (self, product, quantity=1, update_quantity= False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price': str(product.price), 'sell_price': str(product.sell_price)}  
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
           self.cart[product_id]['quantity'] += quantity                 
        self.save()    

    def decrease(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id in self.cart:
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] -= quantity
                if self.cart[product_id]['quantity'] <= 0:
                    del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart 
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()       

    def __iter__(self):
        """ Перебор элементов в корзине и получение продуктов из базы данных."""
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['sell_price'] = Decimal(item['sell_price'])
            item['total_price'] = item['sell_price'] * item['quantity']
            yield item          

    def __len__(self):
        """Общее количество товаров корзине"""
        return sum(item['quantity'] for item in self.cart.values())    

    def get_total_price(self):
        '''Общая стоимость товара в корзине'''
        return sum(Decimal(item['sell_price']) * item['quantity'] for item in
               self.cart.values())    
    
    def clear(self):
        """удаление корзины из сессии"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
