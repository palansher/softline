import os
from flask import Flask
from dotenv import load_dotenv  # Импортируем загрузчик переменных окружения

from routes import main_bp, auth_bp, catalog_bp, cart_bp, admin_bp

load_dotenv(dotenv_path="secrets.env")

app = Flask(__name__)
# app.secret_key = "drivex_super_secret_session_key_2026"

# Загрузка ключа из env
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_development_key")

# МЕНЯЕМ ИМЯ КУКИ
app.config["SESSION_COOKIE_NAME"] = "drivex_session"

# Регистрация Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(admin_bp)


@app.template_filter("format_price")
def format_price(value: float | int | None) -> str:
    if value is None:
        return "0 ₽"
    # Форматируем число с разделением тысяч пробелами, без копеек
    return f"{int(value):,}".replace(",", " ") + " ₽"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8082)
