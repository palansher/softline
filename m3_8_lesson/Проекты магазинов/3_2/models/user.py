from database.connection import query


class UserModel:
    """CRUD-операции над таблицей users."""

    @staticmethod
    def find_by_login(login: str):
        return query(
            "SELECT id, login, pass, phone, role_id FROM users WHERE login = %s",
            (login,), fetchone=True,
        )

    @staticmethod
    def find_by_id(user_id: int):
        return query(
            "SELECT id, login, phone, role_id FROM users WHERE id = %s",
            (user_id,), fetchone=True,
        )

    @staticmethod
    def create(login: str, hashed_password: str, phone: str = "") -> None:
        query(
            "INSERT INTO users (login, pass, phone, role_id) VALUES (%s, %s, %s, 0)",
            (login, hashed_password, phone),
            commit=True,
        )

    @staticmethod
    def login_exists(login: str) -> bool:
        return bool(
            query("SELECT id FROM users WHERE login = %s", (login,), fetchone=True)
        )

    @staticmethod
    def all_with_stats():
        return query("""
            SELECT u.id, u.login, u.phone, u.role_id, u.created_at,
                   COUNT(o.id)                      AS orders_count,
                   COALESCE(SUM(o.total_price), 0)  AS total_spent
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id
            ORDER BY u.created_at DESC
        """, fetchall=True)
