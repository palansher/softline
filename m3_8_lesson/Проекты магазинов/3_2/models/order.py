from database.connection import get_db, query


class OrderModel:
    """Операции с заказами."""

    @staticmethod
    def all_with_users():
        return query("""
            SELECT o.id, o.total_price, o.status,
                   o.phone AS order_phone, o.created_at, o.cart_id,
                   u.login, u.phone AS user_phone, u.id AS user_id
            FROM orders o
            JOIN users u ON o.user_id = u.id
            ORDER BY o.created_at DESC
        """, fetchall=True)

    @staticmethod
    def stats():
        return query("""
            SELECT COUNT(*)                                     AS total_orders,
                   COALESCE(SUM(total_price), 0)               AS total_revenue,
                   COUNT(CASE WHEN status = 'new' THEN 1 END) AS new_orders
            FROM orders
        """, fetchone=True)

    @staticmethod
    def find_by_id_with_user(order_id: int):
        return query("""
            SELECT o.id, o.total_price, o.status,
                   o.phone AS order_phone, o.created_at, o.cart_id,
                   u.login, u.phone AS user_phone, u.id AS user_id
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE o.id = %s
        """, (order_id,), fetchone=True)

    @staticmethod
    def items_for_order(order_id: int):
        return query("""
            SELECT oi.product_name, oi.product_price, oi.quantity,
                   (oi.product_price * oi.quantity) AS subtotal, oi.product_id
            FROM order_items oi
            WHERE oi.order_id = %s
            ORDER BY oi.id
        """, (order_id,), fetchall=True)

    @staticmethod
    def for_user(user_id: int):
        return query("""
            SELECT id, total_price, status, phone, created_at
            FROM orders
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,), fetchall=True)

    @staticmethod
    def update_status(order_id: int, status: str) -> None:
        query(
            "UPDATE orders SET status = %s WHERE id = %s",
            (status, order_id), commit=True,
        )

    @staticmethod
    def create(user_id: int, cart_id: int,
               total_price: float, phone: str, items: list) -> int:
        """
        Создаёт заказ с позициями в одной транзакции.
        Возвращает id нового заказа.
        """
        conn = get_db()
        cur  = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO orders (user_id, cart_id, total_price, phone, status)
                VALUES (%s, %s, %s, %s, 'new') RETURNING id
            """, (user_id, cart_id, total_price, phone))
            order_id = cur.fetchone()[0]

            for item in items:
                cur.execute("""
                    INSERT INTO order_items
                        (order_id, product_id, product_name, product_price, quantity)
                    VALUES (%s, %s, %s, %s, %s)
                """, (order_id, item["product_id"], item["name"],
                      float(item["price"]), item["quantity"]))

            conn.commit()
            return order_id

        except Exception as exc:
            conn.rollback()
            raise exc
        finally:
            cur.close()
            conn.close()
