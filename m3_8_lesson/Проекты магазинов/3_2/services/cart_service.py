from models.cart import CartModel


class CartService:
    """Бизнес-логика работы с корзиной."""

    @staticmethod
    def add_product(user_id: int, product_id: int, qty: int) -> None:
        cart_id  = CartModel.get_or_create(user_id)
        existing = CartModel.find_item(cart_id, product_id)
        if existing:
            CartModel.increment_item(existing["id"], qty)
        else:
            CartModel.add_item(cart_id, product_id, qty)

    @staticmethod
    def get_cart_data(user_id: int) -> dict:
        cart_id = CartModel.get_or_create(user_id)
        items   = CartModel.get_items(cart_id)
        total   = sum(float(i["subtotal"]) for i in items) if items else 0
        return {"cart_id": cart_id, "items": items, "total": total}
