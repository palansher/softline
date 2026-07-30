import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Hello World!</h1>"


# Простая custom-команда
@app.cli.command("init-db")
def init_db():
    """Инициализация базы данных."""
    # Тут может быть логика: db.create_all() или запуск первичных фикстур
    print("База данных успешно инициализирована!")


@app.cli.command("create-admin")
def create_admin():
    """Создать администратора."""
    print("Администратор admin@example.com создан!")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5002"))
    app.run(debug=True, host="0.0.0.0", port=port)
