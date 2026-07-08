import sys
import psycopg2
from werkzeug.security import generate_password_hash

from config import Config
from database.connection import get_db


class DBInitializer:
    """Отвечает за первичную настройку и проверку БД."""

    # ── Публичный API ────────────────────────────────────────

    @classmethod
    def check_connection(cls) -> bool:
        """Проверяет доступность PostgreSQL."""
        cfg = Config.db_config()
        print("\n" + "=" * 50)
        print("🔌 Проверка подключения к PostgreSQL...")
        print(f"   Хост: {cfg['host']}")
        print(f"   Порт: {cfg['port']}")
        print(f"   БД:   {cfg['dbname']}")
        print(f"   Юзер: {cfg['user']}")
        print("=" * 50)

        try:
            conn = psycopg2.connect(**cfg)
            conn.close()
            print("✅ Подключение успешно!\n")
            return True
        except psycopg2.OperationalError as exc:
            cls._print_connection_error(str(exc), cfg)
            return False

    @classmethod
    def ensure_database_exists(cls) -> bool:
        """Создаёт БД, если она ещё не существует."""
        cfg        = Config.db_config().copy()
        target_db  = cfg["dbname"]
        cfg["dbname"] = "postgres"          # системная БД для подключения

        try:
            conn = psycopg2.connect(**cfg)
            conn.autocommit = True
            cur  = conn.cursor()

            cur.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s", (target_db,)
            )
            if cur.fetchone():
                print(f"✅ БД '{target_db}' уже существует")
            else:
                cur.execute(f'CREATE DATABASE "{target_db}"')
                print(f"✅ БД '{target_db}' создана!")

            cur.close()
            conn.close()
            return True

        except psycopg2.OperationalError as exc:
            print(f"❌ Не удалось создать БД: {exc}")
            return False

    @classmethod
    def init_tables(cls) -> None:
        """Создаёт таблицы и наполняет тестовыми данными."""
        conn = get_db()
        cur  = conn.cursor()

        cls._create_tables(cur)
        cls._seed_admin(cur)
        cls._seed_products(cur)

        conn.commit()
        cur.close()
        conn.close()

        print("✅ Таблицы созданы, тестовые данные добавлены")
        print("👤 Админ → login: admin | password: admin123")

    # ── Приватные методы ─────────────────────────────────────

    @staticmethod
    def _create_tables(cur) -> None:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id         SERIAL PRIMARY KEY,
                login      VARCHAR(100) UNIQUE NOT NULL,
                pass       VARCHAR(255) NOT NULL,
                phone      VARCHAR(20)  DEFAULT \'\',
                role_id    INTEGER      DEFAULT 0 CHECK (role_id IN (0, 1)),
                created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id          SERIAL PRIMARY KEY,
                name        VARCHAR(255) NOT NULL,
                description TEXT         DEFAULT \'\',
                price       DECIMAL(10,2) NOT NULL,
                image_url   VARCHAR(500) DEFAULT \'\',
                stock       INTEGER      DEFAULT 0,
                created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id         SERIAL PRIMARY KEY,
                user_id    INTEGER   NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cart_items (
                id         SERIAL PRIMARY KEY,
                cart_id    INTEGER NOT NULL REFERENCES cart(id)     ON DELETE CASCADE,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                quantity   INTEGER DEFAULT 1 CHECK (quantity > 0),
                added_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(cart_id, product_id)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id          SERIAL PRIMARY KEY,
                user_id     INTEGER        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                cart_id     INTEGER        REFERENCES cart(id),
                total_price DECIMAL(10,2)  NOT NULL,
                status      VARCHAR(50)    DEFAULT \'new\',
                phone       VARCHAR(20)    DEFAULT \'\',
                created_at  TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id            SERIAL PRIMARY KEY,
                order_id      INTEGER        NOT NULL REFERENCES orders(id)   ON DELETE CASCADE,
                product_id    INTEGER        NOT NULL REFERENCES products(id),
                product_name  VARCHAR(255)   NOT NULL,
                product_price DECIMAL(10,2)  NOT NULL,
                quantity      INTEGER        NOT NULL CHECK (quantity > 0)
            )
        """)

    @staticmethod
    def _seed_admin(cur) -> None:
        cur.execute("""
            INSERT INTO users (login, pass, phone, role_id)
            VALUES (%s, %s, %s, 1)
            ON CONFLICT (login) DO NOTHING
        """, ("admin", generate_password_hash("admin123"), "+7-000-000-00-00"))

    @staticmethod
    def _seed_products(cur) -> None:
        products = [
            ("iPhone 15 Pro",       "Флагманский смартфон Apple",  129990.00, 50),
            ("Samsung Galaxy S24",  "Флагман Samsung с AI",         89990.00, 30),
            ('MacBook Pro 14"',    "Ноутбук Apple M3 Pro",        199990.00, 20),
            ("AirPods Pro 2",       "Беспроводные наушники Apple",  24990.00, 100),
            ("PlayStation 5",       "Игровая консоль Sony",         49990.00, 15),
            ("Xiaomi Robot Vacuum", "Робот-пылесос с лидаром",      29990.00, 40),
        ]
        for name, desc, price, stock in products:
            cur.execute("""
                INSERT INTO products (name, description, price, stock)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (name, desc, price, stock))

    @staticmethod
    def _print_connection_error(error_msg: str, cfg: dict) -> None:
        print("\n❌ ОШИБКА ПОДКЛЮЧЕНИЯ К POSTGRESQL!")
        print("-" * 50)

        if "Connection refused" in error_msg:
            print("📌 PostgreSQL не запущен")
            print("🔧 net start postgresql-x64-17")
        elif "password authentication failed" in error_msg:
            print("📌 Неверный пароль")
            print(f"🔧 Текущий пароль: '{cfg['password']}'")
        elif "does not exist" in error_msg:
            print(f"📌 БД '{cfg['dbname']}' не существует")
            print(f"🔧 psql -U postgres -c \"CREATE DATABASE {cfg['dbname']};\"")
        elif "could not translate host name" in error_msg:
            print(f"📌 Не удаётся разрешить хост '{cfg['host']}'")
            print("🔧 Попробуйте host=127.0.0.1")
        else:
            print(f"📌 {error_msg}")

        print("=" * 50 + "\n")
