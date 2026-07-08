from database.connection import query


class CartModel:
    """Операции с корзиной и её позициями."""

    @staticmethod
    def get_active(user_id: int):
        """Возвращает активную (не оформленную) корзину пользователя."""
        return query("""
            SELECT c.id FROM cart c
            WHERE c.user_id = %s
              AND c.id NOT IN (
                  SELECT cart_id FROM orders WHERE cart_id IS NOT NULL
              )
            ORDER BY c.created_at DESC LIMIT 1
        """, (user_id,), fetchone=True)

    @staticmethod
    def create(user_id: int) -> int:
        row = query(
            "INSERT INTO cart (user_id) VALUES (%s) RETURNING id",
            (user_id,), fetchone=True, commit=True,
        )
        return row["id"]

    @classmethod
    def get_or_create(cls, user_id: int) -> int:
        cart = cls.get_active(user_id)
        return cart["id"] if cart else cls.create(user_id)

    # ── Позиции ──────────────────────────────────────────────

    @staticmethod
    def get_items(cart_id: int):
        return query("""
            SELECT ci.id, ci.quantity, ci.product_id,
                   p.name, p.price, p.image_url,
                   (p.price * ci.quantity) AS subtotal
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.id
            WHERE ci.cart_id = %s
            ORDER BY ci.added_at
        """, (cart_id,), fetchall=True)

    @staticmethod
    def find_item(cart_id: int, product_id: int):
        return query(
            "SELECT id FROM cart_items WHERE cart_id=%s AND product_id=%s",
            (cart_id, product_id), fetchone=True,
        )

    @staticmethod
    def add_item(cart_id: int, product_id: int, qty: int) -> None:
        query(
            "INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s,%s,%s)",
            (cart_id, product_id, qty), commit=True,
        )

    @staticmethod
    def increment_item(item_id: int, qty: int) -> None:
        query(
            "UPDATE cart_items SET quantity = quantity + %s WHERE id = %s",
            (qty, item_id), commit=True,
        )

    @staticmethod
    def update_item(item_id: int, qty: int, user_id: int) -> None:
        query("""
            UPDATE cart_items SET quantity = %s
            WHERE id = %s
              AND cart_id IN (SELECT id FROM cart WHERE user_id = %s)
        """, (qty, item_id, user_id), commit=True)

    @staticmethod
    def remove_item(item_id: int, user_id: int) -> None:
        query("""
            DELETE FROM cart_items
            WHERE id = %s
              AND cart_id IN (SELECT id FROM cart WHERE user_id = %s)
        """, (item_id, user_id), commit=True)

    @staticmethod
    def clear(cart_id: int) -> None:
        query(
            "DELETE FROM cart_items WHERE cart_id = %s",
            (cart_id,), commit=True,
        )
