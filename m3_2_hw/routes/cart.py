from typing import Any
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from psycopg2.extras import RealDictCursor
from connect_db import connection

# Создаем Blueprint для корзины
cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart")
def cart() -> Any:
    """
    Отображает корзину покупок пользователя.
    Перенаправляет неавторизованных пользователей на страницу входа.
    """
    if not session.get("user_email"):
        flash("Пожалуйста, войдите в систему, чтобы просмотреть корзину.", "warning")
        return redirect(url_for("auth.login"))

    user_id: int = session["user_id"]

    # Получаем корзину пользователя
    sql_cart = "SELECT id FROM carts WHERE user_id = %s;"
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_cart, (user_id,))
        cart_row = cursor.fetchone()

    # Если корзины нет, создаем ее
    if not cart_row:
        sql_create_cart = "INSERT INTO carts (user_id) VALUES (%s) RETURNING id;"
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql_create_cart, (user_id,))
            cart_row = cursor.fetchone()
            connection.commit()

    cart_id: int = cart_row["id"]  # type: ignore

    # Извлекаем товары в корзине
    sql_items = """
        SELECT 
            ci.id AS cart_item_id,
            ci.quantity,
            cat.car_id,
            cat.brand_name,
            cat.model_name,
            cat.price,
            cat.image_small_path
        FROM cart_items ci
        JOIN v_catalog_display cat ON ci.item_id = cat.car_id
        WHERE ci.cart_id = %s;
    """
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_items, (cart_id,))
        items = cursor.fetchall()

    # Получаем данные пользователя, включая адрес для доставки
    sql_user = "SELECT address FROM users WHERE id = %s;"
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_user, (user_id,))
        user_data = cursor.fetchone()

    default_address: str = user_data["address"] if user_data else ""  # type: ignore

    # Вычисляем общую сумму
    total_price: float = sum(float(item["price"]) * item["quantity"] for item in items)

    return render_template("cart.html", items=items, total_price=total_price, default_address=default_address)


@cart_bp.route("/cart/add/<int:car_id>", methods=["POST"])
def add_to_cart(car_id: int) -> Any:
    """
    Добавляет автомобиль в корзину пользователя.
    Если автомобиль уже в корзине, увеличивает количество.
    """
    if not session.get("user_email"):
        flash("Пожалуйста, войдите в систему, чтобы добавлять товары в корзину.", "warning")
        return redirect(url_for("auth.login"))

    user_id: int = session["user_id"]

    # Находим ID корзины пользователя
    sql_cart = "SELECT id FROM carts WHERE user_id = %s;"
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_cart, (user_id,))
        cart = cursor.fetchone()

    # Если корзины по какой-то причине нет, создаем ее на лету
    if not cart:
        sql_create_cart = "INSERT INTO carts (user_id) VALUES (%s) RETURNING id;"
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql_create_cart, (user_id,))
            cart = cursor.fetchone()
            connection.commit()

    cart_id: int = cart["id"]  # type: ignore

    # Добавляем или обновляем количество товара в корзине
    sql_add = """
        INSERT INTO cart_items (cart_id, item_id, quantity)
        VALUES (%s, %s, 1)
        ON CONFLICT (cart_id, item_id)
        DO UPDATE SET quantity = cart_items.quantity + 1;
    """
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_add, (cart_id, car_id))
        connection.commit()

    flash("Автомобиль успешно добавлен в корзину!", "success")
    return redirect(url_for("cart.cart"))


@cart_bp.route("/cart/remove/<int:cart_item_id>", methods=["POST"])
def remove_from_cart(cart_item_id: int) -> Any:
    """
    Удаляет товар из корзины.
    """
    if not session.get("user_email"):
        return redirect(url_for("auth.login"))

    user_id: int = session["user_id"]

    # Проверяем, что корзина принадлежит текущему пользователю
    sql_delete = """
        DELETE FROM cart_items 
        WHERE id = %s AND cart_id IN (SELECT id FROM carts WHERE user_id = %s);
    """
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_delete, (cart_item_id, user_id))
        connection.commit()

    flash("Товар удален из корзины.", "info")
    return redirect(url_for("cart.cart"))


@cart_bp.route("/cart/update/<int:cart_item_id>", methods=["POST"])
def update_cart_quantity(cart_item_id: int) -> Any:
    """
    Обновляет количество конкретного товара в корзине.
    Если запрошенное количество 0 или меньше, товар удаляется из корзины.
    """
    if not session.get("user_email"):
        return redirect(url_for("auth.login"))

    user_id: int = session["user_id"]
    quantity_str = request.form.get("quantity", "1")

    try:
        quantity = int(quantity_str)
        if quantity <= 0:
            sql_delete = """
                DELETE FROM cart_items 
                WHERE id = %s AND cart_id IN (SELECT id FROM carts WHERE user_id = %s);
            """
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(sql_delete, (cart_item_id, user_id))
                connection.commit()
            flash("Товар удален из корзины.", "info")
        else:
            sql_update = """
                UPDATE cart_items 
                SET quantity = %s 
                WHERE id = %s AND cart_id IN (SELECT id FROM carts WHERE user_id = %s);
            """
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(sql_update, (quantity, cart_item_id, user_id))
                connection.commit()
            flash("Количество товара обновлено.", "success")
    except ValueError:
        flash("Некорректное значение количества.", "danger")

    return redirect(url_for("cart.cart"))


@cart_bp.route("/cart/order", methods=["POST"])
def place_order() -> Any:
    """
    Оформляет заказ из корзины покупок пользователя.
    Создает записи в таблицах orders и order_items, а также очищает cart_items.
    """
    if not session.get("user_email"):
        return redirect(url_for("auth.login"))

    user_id: int = session["user_id"]
    shipping_address: str = request.form.get("shipping_address", "").strip()

    if not shipping_address:
        flash("Пожалуйста, укажите адрес доставки.", "danger")
        return redirect(url_for("cart.cart"))

    # Находим ID корзины пользователя
    sql_cart = "SELECT id FROM carts WHERE user_id = %s;"
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_cart, (user_id,))
        cart_row = cursor.fetchone()

    if not cart_row:
        flash("Ваша корзина пуста.", "warning")
        return redirect(url_for("cart.cart"))

    cart_id: int = cart_row["id"]  # type: ignore

    # Извлекаем все товары из корзины для переноса в заказ
    sql_items = """
        SELECT ci.item_id, ci.quantity, cat.price
        FROM cart_items ci
        JOIN v_catalog_display cat ON ci.item_id = cat.car_id
        WHERE ci.cart_id = %s;
    """
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_items, (cart_id,))
        cart_items = cursor.fetchall()

    if not cart_items:
        flash("В корзине нет товаров для оформления заказа.", "warning")
        return redirect(url_for("cart.cart"))

    total_amount: float = sum(float(item["price"]) * item["quantity"] for item in cart_items)

    try:
        # Отключаем autocommit, чтобы выполнить создание заказа и очистку корзины в одной транзакции
        connection.autocommit = False
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            # Создаем заказ
            sql_insert_order = """
                INSERT INTO orders (user_id, status, total_amount, discount_amount, shipping_address)
                VALUES (%s, 0, %s, 0.00, %s)
                RETURNING id;
            """
            cursor.execute(sql_insert_order, (user_id, total_amount, shipping_address))
            order_id: int = cursor.fetchone()["id"]  # type: ignore

            # Переносим товары из корзины в order_items
            sql_insert_item = """
                INSERT INTO order_items (order_id, catalog_id, price, quantity)
                VALUES (%s, %s, %s, %s);
            """
            for item in cart_items:
                cursor.execute(sql_insert_item, (order_id, item["item_id"], item["price"], item["quantity"]))

            # Очищаем корзину
            sql_clear_cart = "DELETE FROM cart_items WHERE cart_id = %s;"
            cursor.execute(sql_clear_cart, (cart_id,))

        connection.commit()
        flash("Заказ успешно оформлен!", "success")
        return redirect(url_for("cart.order_success", order_id=order_id))
    except Exception:
        connection.rollback()
        flash("Произошла ошибка при оформлении заказа. Пожалуйста, попробуйте снова.", "danger")
        return redirect(url_for("cart.cart"))
    finally:
        connection.autocommit = True


@cart_bp.route("/order-success/<int:order_id>")
def order_success(order_id: int) -> Any:
    """
    Отображает страницу успешного оформления заказа с текущими деталями заказа и его статусом.
    """
    if not session.get("user_email"):
        return redirect(url_for("auth.login"))

    user_id: int = session["user_id"]

    # Извлекаем информацию о заказе
    sql_order = """
        SELECT o.id, o.status, o.total_amount, o.shipping_address, o.created_at, os.name AS status_name
        FROM orders o
        JOIN order_statuses os ON o.status = os.id
        WHERE o.id = %s AND o.user_id = %s;
    """
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_order, (order_id, user_id))
        order = cursor.fetchone()

    if not order:
        flash("Заказ не найден.", "danger")
        return redirect(url_for("main.index"))

    # Извлекаем элементы заказа напрямую через catalog и brand таблицы
    sql_order_items = """
        SELECT oi.quantity, oi.price, b.name AS brand_name, c.model AS model_name, c.image_small_path
        FROM order_items oi
        JOIN catalog c ON oi.catalog_id = c.id
        JOIN brand b ON c.brand_id = b.id
        WHERE oi.order_id = %s;
    """
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_order_items, (order_id,))
        items = cursor.fetchall()

    return render_template("order-success.html", order=order, items=items)
