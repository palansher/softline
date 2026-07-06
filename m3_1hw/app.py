from flask import Flask, render_template, request
from connect_db import cursor

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("main.html")


@app.route("/contacts")
def contacts() -> str:
    return render_template("contacts.html")



# def catalog() -> str:
#     return render_template("catalog.html")

@app.route("/catalog")
def catalog():

    sql = "SELECT * FROM v_catalog_display ORDER BY price DESC;"
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template("catalog.html", items=data)

@app.template_filter('format_price')
def format_price(value):
    if value is None:
        return "0 ₽"
    # Форматируем число с разделением тысяч пробелами, без копеек
    return f"{int(value):,}".replace(",", " ") + " ₽"

# <p class="text-muted">{{ car.full_info | linebreaksbr }}</p>
# фильтр linebreaksbr автоматически заменит обычные переносы строк на теги <br>

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8082)
