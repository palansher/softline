from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("main.html")


@app.route("/contacts")
def contacts() -> str:
    return render_template("contacts.html")


@app.route("/catalog")
def catalog() -> str:
    return render_template("catalog.html")

# <p class="text-muted">{{ car.full_info | linebreaksbr }}</p>
# фильтр linebreaksbr автоматически заменит обычные переносы строк на теги <br>

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8082)
