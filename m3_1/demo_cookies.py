from flask import Flask, request, redirect, make_response


# макс размер куки в браузере - 4 Кб

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    res = make_response("Создание объекта для cookie")
    res.set_cookie("fio", "Иванов Иван", max_age=3600 * 24 * 365 * 2)
    return redirect("/show_cookie")


@app.route("/show_cookie")
def show_cookie():
    return "Привет, " + request.cookies.get("fio", "")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8084)
