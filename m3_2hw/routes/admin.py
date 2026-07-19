from typing import Any
from flask import Blueprint, render_template, redirect, url_for, session, flash, abort
from psycopg2.extras import RealDictCursor
from connect_db import connection

# Создаем Blueprint для админки
admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
def admin() -> Any:
    """
    Displays the admin panel showing all orders with buyer details and item details.
    Restricted to users with role_id = 1.
    """
    
    # Выводим всё содержимое сессии в консоль терминала для отладки
    print("--- ТЕКУЩАЯ СЕССИЯ Flask ---")
    print(dict(session)) 
    print("----------------------------")

    # Или проверяем конкретные ключи
    user_email = session.get("user_email")
    role_id = session.get("role_id")
    print(f"Пользователь: {user_email}, Роль: {role_id}")
    
    if not session.get("user_email"):
        flash("Пожалуйста, войдите в систему.", "warning")
        return redirect(url_for("auth.login"))

    if session.get("role_id") != 1:
        abort(403)  # Forbidden

    # Получаем все заказы с информацией о покупателях
    sql_orders = """
        SELECT 
            o.id AS order_id,
            o.user_id,
            o.status,
            o.total_amount,
            o.shipping_address,
            o.created_at,
            u.full_name AS buyer_name,
            u.email AS buyer_email,
            u.phone AS buyer_phone,
            os.name AS status_name
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN order_statuses os ON o.status = os.id
        ORDER BY o.created_at DESC;
    """
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_orders)
        orders = cursor.fetchall()

    # Получаем все товары всех заказов
    sql_items = """
        SELECT 
            oi.order_id,
            oi.quantity,
            oi.price,
            b.name AS brand_name,
            c.model AS model_name
        FROM order_items oi
        JOIN catalog c ON oi.catalog_id = c.id
        JOIN brand b ON c.brand_id = b.id;
    """
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_items)
        all_items = cursor.fetchall()

    # Группируем товары по id заказа
    items_by_order: dict[int, list[dict]] = {}
    for item in all_items:
        order_id = item["order_id"]  # type: ignore
        if order_id not in items_by_order:
            items_by_order[order_id] = []
        items_by_order[order_id].append(item)

    # Присоединяем товары к заказам
    for order in orders:
        order["items"] = items_by_order.get(order["order_id"], [])  # type: ignore

    return render_template("admin.html", orders=orders)
