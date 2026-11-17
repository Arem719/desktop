from decimal import Decimal

from .models import Product

SESSION_KEY = "cart"


class Cart:
    """Session cart: {product_id: quantity}. Works for guests and users."""

    def __init__(self, request):
        self.session = request.session
        self.data = self.session.setdefault(SESSION_KEY, {})

    def _save(self):
        self.session.modified = True

    def add(self, product, quantity=1):
        key = str(product.pk)
        new_qty = self.data.get(key, 0) + quantity
        self.set(product, new_qty)

    def set(self, product, quantity):
        key = str(product.pk)
        quantity = min(max(int(quantity), 0), product.stock)
        if quantity:
            self.data[key] = quantity
        else:
            self.data.pop(key, None)
        self._save()

    def remove(self, product):
        self.data.pop(str(product.pk), None)
        self._save()

    def clear(self):
        self.session[SESSION_KEY] = {}
        self._save()

    def __iter__(self):
        products = Product.objects.filter(pk__in=self.data.keys(), is_active=True)
        for p in products:
            qty = self.data[str(p.pk)]
            yield {"product": p, "quantity": qty, "subtotal": p.price * qty}

    def __len__(self):
        return sum(self.data.values())

    @property
    def total(self):
        return sum((i["subtotal"] for i in self), Decimal("0"))
