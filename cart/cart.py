# from django.conf import settings
from shop.models import Product
# cart.py

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart



    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id not in self.cart:
            self.cart[product_id] =  int(product_qty)
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def get_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0

        for key, value in self.cart.items():
            key = int(key)
            for product in products :
                if product.id == key:
                    if product.is_sale :
                        total += (product.sale_price * value)
                    else:
                        total += (product.price * value)
        return total
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart
        ourcart[product_id] = product_qty
        self.session.modified = True
        r = self.cart
        return r

    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True


