from flask import Blueprint, render_template

# Создаем Blueprint для простых страниц без кода
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index() -> str:
    """
    Рендерит главную страницу сайта.
    """
    return render_template("main.html")


@main_bp.route("/contacts")
def contacts() -> str:
    """
    Рендерит страницу контактов сайта.
    """
    return render_template("contacts.html")
