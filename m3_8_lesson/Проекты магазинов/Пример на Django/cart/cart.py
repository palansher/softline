"""Корзина покупок на основе Django Session."""

from decimal import Decimal

from django.conf import settings

from main.models import Product


class Cart:
    """Корзина хранится в сессии пользователя по ключу ``CART_SESSION_ID``.

    Каждая запись — словарь с ключом ``product_id``, содержащий количество
    и цену товара на момент добавления.
    """

    def __init__(self, request):
        """Инициализация корзины из сессии .

        Если сессия пуста, создаётся пустой словарь для корзины.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Добавить товара в корзину."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """Отметить сессию как изменённую."""
        self.session.modified = True

    def remove(self, product):
        """Удалить товар из корзины."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def __iter__(self):
        """Итерировать по товарам корзины, обогащая данными из БД."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart_copy = self.cart.copy()
        for product in products:
            cart_copy[str(product.id)]['product'] = product

        for item in cart_copy.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Общее количество позиций в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Суммарная стоимость всех товаров."""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        """Очистить корзину полностью."""
        del self.session[settings.CART_SESSION_ID]
        self.save()
