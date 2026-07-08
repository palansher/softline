from database.connection import query


class ProductModel:
    """CRUD-операции над таблицей products."""

    @staticmethod
    def all():
        return query("SELECT * FROM products ORDER BY id", fetchall=True)

    @staticmethod
    def find_by_id(product_id: int):
        return query(
            "SELECT * FROM products WHERE id = %s",
            (product_id,), fetchone=True,
        )
