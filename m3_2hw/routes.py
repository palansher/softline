from typing import Union, Any
from flask import Blueprint, render_template, g
from psycopg2.extras import RealDictCursor
from connect_db import get_db

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index() -> str:
    return render_template("main.html")

@main_bp.route("/contacts")
def contacts() -> str:
    return render_template("contacts.html")

@main_bp.route("/catalog")
def catalog() -> str:
    sql = "SELECT * FROM v_catalog_display ORDER BY price DESC;"
    
    connection = get_db()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
    
    # Явный коммит, как просил пользователь
    connection.commit()
    
    return render_template("catalog.html", items=data)

@main_bp.route("/catalog/<int:car_id>")
def car_detail(car_id: int) -> Union[str, tuple[str, int]]:
    sql = "SELECT * FROM v_catalog_display WHERE car_id = %s;"

    connection = get_db()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql, (car_id,))
        car = cursor.fetchone()

    # Явный коммит
    connection.commit()

    if not car:
        return "Автомобиль не найден", 404

    return render_template("car-detail.html", car=car)

@main_bp.app_template_filter("format_price")
def format_price(value):
    if value is None:
        return "0 ₽"
    return f"{int(value):,}".replace(",", " ") + " ₽"
