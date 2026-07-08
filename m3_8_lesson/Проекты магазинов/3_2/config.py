import os

class Config:
    """Базовая конфигурация приложения."""

    # ── База данных ──────────────────────────────────────────
    DB_HOST     = os.environ.get("DB_HOST",     "localhost")
    DB_PORT     = os.environ.get("DB_PORT",     "5432")
    DB_NAME     = os.environ.get("DB_NAME",     "shop_db")
    DB_USER     = os.environ.get("DB_USER",     "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "123")

    @classmethod
    def db_config(cls) -> dict:
        return {
            "host":     cls.DB_HOST,
            "port":     cls.DB_PORT,
            "dbname":   cls.DB_NAME,
            "user":     cls.DB_USER,
            "password": cls.DB_PASSWORD,
        }

    # ── Flask ────────────────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "123")
    DEBUG      = os.environ.get("DEBUG", "true").lower() == "true"
    PORT       = int(os.environ.get("PORT", 5000))
