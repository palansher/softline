from urllib.parse import quote, unquote 
from flask import Flask, request, redirect, make_response

"""
Почему была проблема с 

@app.route("/", methods=["GET", "POST"])
def index():
    res = make_response("Создание объекта для cookie")
    res.set_cookie("fio", "Иванов Иван", max_age=3600 * 24 * 365 * 2)
    return redirect("/show_cookie")


Почему это происходит:
Контекст Flask: Когда функция index() возвращает простую строку "Hello, World!", 
Flask автоматически генерирует для нее новый, чистый HTTP-ответ без каких-либо заголовков Set-Cookie.
Переменная res: Созданный ранее объект res оставался локальной переменной внутри функции и уничтожался после выполнения return.
"""

"""
Как исправлено:

redirect() внутри make_response():
    Чтобы куки прикрепились к перенаправлению, 
    нужно передавать функцию redirect() прямо внутрь make_response()

quote() и unquote(): 
    Эти функции превращают русские буквы в безопасный набора символов %XX и возвращают их обратно.
    Это гарантирует, что браузер не потеряет и не заблокирует данные.
"""


# Импортируем инструменты для кодирования текста в URL-формат
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Перенаправление на страницу просмотра
    res = make_response(redirect('/show_cookie'))
    
    # Кодируем "Иванов Иван" в ASCII-безопасную строку (например, %D0%98%D0%B2...)
    encoded_name = quote('Иванов Иван')
    
    res.set_cookie('fio', encoded_name, max_age=3600 * 24 * 365 * 2)
    return res

@app.route('/show_cookie')
def show_cookie():
    # Получаем закодированную строку из куки
    cookie_value = request.cookies.get('fio', "")
    
    # Декодируем её обратно в нормальный текст
    decoded_name = unquote(cookie_value)
    
    return 'Привет, ' + decoded_name


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8084)
