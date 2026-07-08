from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "GET":
        return """<form method="post">
                <p>Введите Ваше имя</p>
                <input type="text" name="fio">
            
                <p>Введите Ваш возраст</p>
                <input type="number" name="age"><br><br>
                <input type="submit" value="Сохранить">
            </form>"""
    fio = request.form.get("fio", "")
    age = request.form.get("age", "")
    if not fio or not age:
        return "Вы не заполнили форму"
    age = int(age)
    return f"Добрый день, {fio}, Ваш возраст: {age}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
