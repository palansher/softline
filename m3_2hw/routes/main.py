from flask import Blueprint, render_template

# Создаем Blueprint для основных страниц
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index() -> str:
    """
    Renders the home page of the website.
    """
    return render_template("main.html")


@main_bp.route("/contacts")
def contacts() -> str:
    """
    Renders the contacts page of the website.
    """
    return render_template("contacts.html")
