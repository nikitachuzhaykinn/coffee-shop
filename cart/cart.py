from decimal import Decimal
from django.conf import settings
from catalog.models import Product, ModifierOption

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, modifier_options=None):
        modifier_options = modifier_options or []
        sorted_mods = sorted([int(m) for m in modifier_options])
        
        mods_str = "_".join(str(m) for m in sorted_mods)
        product_key = f"{product.id}_{mods_str}"
        
        if product_key in self.cart:
            self.cart[product_key]['quantity'] += quantity
        else:
            self.cart[product_key] = {
                'quantity': quantity,
                'modifiers': sorted_mods
            }
        self.save()

    def remove(self, product_key):
        if product_key in self.cart:
            del self.cart[product_key]
            self.save()

    def update_quantity(self, product_key, quantity):
        if product_key in self.cart:
            self.cart[product_key]['quantity'] = int(quantity)
            if self.cart[product_key]['quantity'] <= 0:
                self.remove(product_key)
            else:
                self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        total = Decimal('0')
        for item_data in self:
            total += item_data['total_price']
        return total

    def get_total_items(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = [key.split('_')[0] for key in self.cart.keys()]
        products = {p.id: p for p in Product.objects.filter(id__in=product_ids)}
        
        for key, item_data in self.cart.items():
            product_id = int(key.split('_')[0])
            product = products.get(product_id)
            if not product:
                continue
            
            # ВАЖНО: Создаем копию, чтобы не мутировать исходный словарь в сессии!
            item = item_data.copy()
            
            modifier_ids = item['modifiers']
            modifiers = ModifierOption.objects.filter(id__in=modifier_ids)
            
            modifiers_price = sum(m.price_extra for m in modifiers)
            base_price = product.price
            
            item['product'] = product
            item['modifiers'] = list(modifiers)
            item['key'] = key
            item['total_price'] = (base_price + modifiers_price) * item['quantity']
            item['unit_price'] = base_price + modifiers_price
            yield item