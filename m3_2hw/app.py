from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, Response
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

# from connect_db import cursor  # , connection
from connect_db import connection  # Импортируем соединение вместо курсора

app = Flask(__name__)
app.secret_key = "drivex_super_secret_session_key_2026"


@app.route("/")
def index() -> str:
    return render_template("main.html")


@app.route("/contacts")
def contacts() -> str:
    return render_template("contacts.html")


@app.route("/register", methods=["GET", "POST"])
def register() -> str | Response:
    """
    Handles user registration.
    Saves user email, password (hashed), full_name, phone, address.
    Assigns role_id = 0 (user) and creates a cart in the same transaction.
    """
    if session.get("user_email"):
        return redirect(url_for("index"))

    if request.method == "POST":
        email: str = request.form.get("email", "").strip()
        password: str = request.form.get("password", "").strip()
        full_name: str = request.form.get("full_name", "").strip()
        phone: str = request.form.get("phone", "").strip()
        address: str = request.form.get("address", "").strip()

        if not email or not password or not full_name or not phone or not address:
            flash("Пожалуйста, заполните все поля формы.", "danger")
            return render_template("register.html")

        # Проверяем, существует ли уже пользователь с таким email
        sql_check = "SELECT id FROM users WHERE email = %s;"
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql_check, (email,))
            user_exists = cursor.fetchone()

        if user_exists:
            flash("Пользователь с таким email уже зарегистрирован.", "danger")
            return render_template("register.html")

        password_hash: str = generate_password_hash(password)

        try:
            # Отключаем autocommit, чтобы выполнить обе вставки в одной транзакции
            connection.autocommit = False
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Вставляем пользователя
                sql_insert_user = """
                    INSERT INTO users (email, password_hash, full_name, phone, address, role_id)
                    VALUES (%s, %s, %s, %s, %s, 0)
                    RETURNING id;
                """
                cursor.execute(sql_insert_user, (email, password_hash, full_name, phone, address))
                user_id: int = cursor.fetchone()["id"]

                # Создаем пустую корзину для этого пользователя
                sql_insert_cart = """
                    INSERT INTO carts (user_id)
                    VALUES (%s);
                """
                cursor.execute(sql_insert_cart, (user_id,))

            connection.commit()
            flash("Регистрация прошла успешно! Теперь вы можете войти.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            connection.rollback()
            flash("Произошла ошибка при регистрации. Пожалуйста, попробуйте еще раз.", "danger")
            return render_template("register.html")
        finally:
            connection.autocommit = True

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    """
    Handles user authentication.
    Validates user credentials against password hash.
    Saves user_id, user_email, and role_id in session upon successful login.
    """
    if session.get("user_email"):
        return redirect(url_for("index"))

    if request.method == "POST":
        email: str = request.form.get("email", "").strip()
        password: str = request.form.get("password", "").strip()

        if not email or not password:
            flash("Пожалуйста, заполните все поля.", "danger")
            return render_template("login.html")

        sql_user = "SELECT id, email, password_hash, role_id FROM users WHERE email = %s;"
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql_user, (email,))
            user = cursor.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_email"] = user["email"]
            session["role_id"] = user["role_id"]
            flash("Вы успешно вошли в систему!", "success")
            return redirect(url_for("catalog"))
        else:
            flash("Неверный email или пароль.", "danger")
            return render_template("login.html")

    return render_template("login.html")


@app.route("/logout")
def logout() -> Response:
    """
    Logs out the user by clearing the session data.
    """
    session.clear()
    flash("Вы успешно вышли из системы.", "info")
    return redirect(url_for("index"))


@app.route("/catalog")
def catalog() -> str:
    """
    Displays the catalog of available cars.
    """
    sql = "SELECT * FROM v_catalog_display ORDER BY price DESC;"

    # Создаем локальный курсор для конкретного запроса
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()

    # Здесь курсор уже автоматически и безопасно закрылся
    return render_template("catalog.html", items=data)


@app.route("/catalog/<int:car_id>")
def car_detail(car_id: int) -> str | tuple[str, int]:
    """
    Displays details for a specific car.
    """
    # Запрашиваем из VIEW конкретную машину по id
    sql = "SELECT * FROM v_catalog_display WHERE car_id = %s;"

    # Создаем локальный курсор для конкретного просмотра машины
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql, (car_id,))
        car = cursor.fetchone()

    # Если машина не найдена (например, ввели неверный ID в URL), отдаем ошибку 404
    if not car:
        return "Автомобиль не найден", 404

    return render_template("car-detail.html", car=car)


@app.route("/cart/add/<int:car_id>", methods=["POST"])
def add_to_cart(car_id: int) -> Response:
    """
    Adds a car to the user's cart.
    If the car is already in the cart, increments the quantity.
    """
    if not session.get("user_email"):
        flash("Пожалуйста, войдите в систему, чтобы добавлять товары в корзину.", "warning")
        return redirect(url_for("login"))

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

    cart_id: int = cart["id"]

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
    return redirect(url_for("cart"))


@app.route("/cart/remove/<int:cart_item_id>", methods=["POST"])
def remove_from_cart(cart_item_id: int) -> Response:
    """
    Removes an item from the cart.
    """
    if not session.get("user_email"):
        return redirect(url_for("login"))

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
    return redirect(url_for("cart"))


@app.route("/cart")
def cart() -> str | Response:
    """
    Displays the user's shopping cart.
    Redirects unauthenticated users to the login page.
    """
    if not session.get("user_email"):
        flash("Пожалуйста, войдите в систему, чтобы просмотреть корзину.", "warning")
        return redirect(url_for("login"))

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

    cart_id: int = cart_row["id"]

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

    default_address: str = user_data["address"] if user_data else ""

    # Вычисляем общую сумму
    total_price: float = sum(float(item["price"]) * item["quantity"] for item in items)

    return render_template("cart.html", items=items, total_price=total_price, default_address=default_address)


@app.route("/cart/order", methods=["POST"])
def place_order() -> Response:
    """
    Places an order from the user's shopping cart.
    Creates records in orders and order_items tables, and clears cart_items.
    """
    if not session.get("user_email"):
        return redirect(url_for("login"))

    user_id: int = session["user_id"]
    shipping_address: str = request.form.get("shipping_address", "").strip()

    if not shipping_address:
        flash("Пожалуйста, укажите адрес доставки.", "danger")
        return redirect(url_for("cart"))

    # Находим ID корзины пользователя
    sql_cart = "SELECT id FROM carts WHERE user_id = %s;"
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_cart, (user_id,))
        cart_row = cursor.fetchone()

    if not cart_row:
        flash("Ваша корзина пуста.", "warning")
        return redirect(url_for("cart"))

    cart_id: int = cart_row["id"]

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
        return redirect(url_for("cart"))

    total_amount: float = sum(float(item["price"]) * item["quantity"] for item in cart_items)

    try:
        # Отключаем autocommit, чтобы выполнить создание заказа и очистку корзины в одной транзакции
        connection.autocommit = False
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            # 1. Создаем заказ
            sql_insert_order = """
                INSERT INTO orders (user_id, status, total_amount, discount_amount, shipping_address)
                VALUES (%s, 0, %s, 0.00, %s)
                RETURNING id;
            """
            cursor.execute(sql_insert_order, (user_id, total_amount, shipping_address))
            order_id: int = cursor.fetchone()["id"]

            # 2. Переносим товары из корзины в order_items
            sql_insert_item = """
                INSERT INTO order_items (order_id, catalog_id, price, quantity)
                VALUES (%s, %s, %s, %s);
            """
            for item in cart_items:
                cursor.execute(sql_insert_item, (order_id, item["item_id"], item["price"], item["quantity"]))

            # 3. Очищаем корзину
            sql_clear_cart = "DELETE FROM cart_items WHERE cart_id = %s;"
            cursor.execute(sql_clear_cart, (cart_id,))

        connection.commit()
        flash("Заказ успешно оформлен!", "success")
        return redirect(url_for("order_success", order_id=order_id))
    except Exception as e:
        connection.rollback()
        flash("Произошла ошибка при оформлении заказа. Пожалуйста, попробуйте снова.", "danger")
        return redirect(url_for("cart"))
    finally:
        connection.autocommit = True


@app.route("/order-success/<int:order_id>")
def order_success(order_id: int) -> str | Response:
    """
    Displays the order success page with current order details and its status.
    """
    if not session.get("user_email"):
        return redirect(url_for("login"))

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
        return redirect(url_for("index"))

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


@app.route("/admin")
def admin() -> str | Response:
    """
    Displays the admin panel showing all orders with buyer details and item details.
    Restricted to users with role_id = 1.
    """
    if not session.get("user_email"):
        flash("Пожалуйста, войдите в систему.", "warning")
        return redirect(url_for("login"))

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
        order_id = item["order_id"]
        if order_id not in items_by_order:
            items_by_order[order_id] = []
        items_by_order[order_id].append(item)

    # Присоединяем товары к заказам
    for order in orders:
        order["items"] = items_by_order.get(order["order_id"], [])

    return render_template("admin.html", orders=orders)


@app.template_filter("format_price")
def format_price(value: float | int | None) -> str:
    if value is None:
        return "0 ₽"
    # Форматируем число с разделением тысяч пробелами, без копеек
    return f"{int(value):,}".replace(",", " ") + " ₽"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8082)
