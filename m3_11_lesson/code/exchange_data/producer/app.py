from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

CONSUMER_URL = "http://consumer:4001/process"

HTML_FORM = '''
<h1>Сервис Producer</h1>
<form action="/send" method="post">
    <p>Введите текст</p>
    <input type="text" name="data"><br>
    <button type="submit">Отправить в Consumer</button>
</form>

<h1>Результат: {{ result }}</h1>
'''


@app.route("/")
def index():
    return render_template_string(HTML_FORM, result="")


@app.route("/send", methods=['POST'])
def send():
    data = request.form.get("data")
    if not data:
        return "Ошибка: нет данных", 400
    try:
        response = requests.post(
            CONSUMER_URL,
            json={"input_data": data},
            headers={"Content-Type": "application/json"}
        )
        result = response.json().get("result", "Ошибка")
    except Exception as e:
        result = f"Ошибка связи с сервисом Консьюмер: {str(e)}"

    return render_template_string(HTML_FORM, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)