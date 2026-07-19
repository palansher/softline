from flask import Flask

from routes import main_bp, auth_bp, catalog_bp, cart_bp, admin_bp

app = Flask(__name__)
app.secret_key = "drivex_super_secret_session_key_2026"

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
