import sys
from flask import Flask
from config import Config
from database.initializer import DBInitializer
from routes.auth   import auth_bp
from routes.shop   import shop_bp
from routes.cart   import cart_bp
from routes.orders import orders_bp
from routes.admin  import admin_bp


def create_app() -> Flask:
    """Фабрика приложения Flask."""
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY

    # Регистрация blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)

    return app


if __name__ == "__main__":
    if not DBInitializer.check_connection():
        print("🛑 Запуск остановлен. Исправьте подключение к БД.")
        sys.exit(1)

    DBInitializer.ensure_database_exists()
    DBInitializer.init_tables()

    app = create_app()

    print("\n🚀 Запуск Flask-сервера...")
    print("📌 Откройте браузер: http://127.0.0.1:5000")
    print("👤 Админ: login=admin | password=admin123")
    print("=" * 50 + "\n")

    app.run(debug=Config.DEBUG, port=Config.PORT)
