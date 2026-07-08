from models.cart import CartModel
from models.order import OrderModel


class OrderService:
    """Бизнес-логика оформления заказов."""

    @staticmethod
    def create_from_cart(user_id: int, phone: str) -> int:
        """
        Оформляет заказ из активной корзины.
        Возвращает id нового заказа.
        Бросает ValueError если корзина пуста.
        """
        cart_id = CartModel.get_or_create(user_id)
        items   = CartModel.get_items(cart_id)

        if not items:
            raise ValueError("Корзина пуста")

        total = sum(float(i["subtotal"]) for i in items)
        order_id = OrderModel.create(user_id, cart_id, total, phone, items)
        CartModel.clear(cart_id)
        return order_id
