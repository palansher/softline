from flask import Flask, render_template
from psycopg2.extras import RealDictCursor

# from connect_db import cursor  # , connection
from connect_db import connection  # Импортируем соединение вместо курсора

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("main.html")


@app.route("/contacts")
def contacts() -> str:
    return render_template("contacts.html")


@app.route("/catalog")
def catalog():

    sql = "SELECT * FROM v_catalog_display ORDER BY price DESC;"
    # cursor.execute(sql)

    # Создаем локальный курсор для конкретного запроса
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()

    # Здесь курсор уже автоматически и безопасно закрылся
    return render_template("catalog.html", items=data)


@app.route("/catalog/<int:car_id>")
def car_detail(car_id: int):
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


@app.template_filter("format_price")
def format_price(value):
    if value is None:
        return "0 ₽"
    # Форматируем число с разделением тысяч пробелами, без копеек
    return f"{int(value):,}".replace(",", " ") + " ₽"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8082)
