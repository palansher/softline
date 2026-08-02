from flask import Blueprint, render_template
from psycopg2.extras import RealDictCursor
from connect_db import connection

# Создаем Blueprint для каталога
catalog_bp = Blueprint("catalog", __name__)


@catalog_bp.route("/catalog")
def catalog() -> str:
    """
    Отображает каталог доступных автомобилей.
    """
    sql = "SELECT * FROM v_catalog_display ORDER BY price DESC;"

    # Создаем локальный курсор для конкретного запроса
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()

    return render_template("catalog.html", items=data)


@catalog_bp.route("/catalog/<int:car_id>")
def car_detail(car_id: int) -> str | tuple[str, int]:
    """
    Отображает подробную информацию о конкретном автомобиле.
    """
    sql = "SELECT * FROM v_catalog_display WHERE car_id = %s;"

    # Создаем локальный курсор для конкретного просмотра машины
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql, (car_id,))
        car = cursor.fetchone()

    if not car:
        return "Автомобиль не найден", 404

    return render_template("car-detail.html", car=car)
