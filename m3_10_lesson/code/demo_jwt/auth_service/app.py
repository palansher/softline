from flask import Flask, request, jsonify
# Модуль для загрузки системных переменных из файла .env
from dotenv import load_dotenv
import os
import jwt
import datetime
# Импорт декоратора wraps для сохранения метаданных функций(например, название)
from functools import wraps

# Загружаем системные переменные из файла .env
load_dotenv()
app = Flask(__name__)

# Получение секретного ключа
SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    SECRET_KEY = "LKSJDKLFJDSLFJsgfdflgj3920342/*/sdfljgklasdfsg-23rsldkak"

# Список юзеров, которые могут войти в систему
USERS = {
    "admin":"pass123",
    "user":"123",
}


# Создаем декоратор для проверки валидности токена. То есть
# будем в дальнейшем данный декоратор устанавливать перед функциями,
# которые не доступны для всех

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Извлекаем токен из заголовка Authorization
        # в формате Bearer<token>
        if 'Authorization' in request.headers:
            # Берем только сам токен, разбивая строку по пробелу
            token = request.headers['Authorization'].split(" ")[1]
            if not token:
                return jsonify({'message': 'Token is missing'}),401
            try:
                # Декодируем и верифицируем токен с использованием секретного ключа
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                login = payload['login']
            # Если срок жизни токена истек
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Срок жизни токена истек!'}),401

            # токен недействителен, пытаются подделать
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Токен невалидный!'}),401
            return f(login, *args, **kwargs)
    return decorated

@app.route("/login", methods=["POST"])
def login():
    """Выписываем токен при успешной аутентификации"""
    # Получаем логин и пароль из тела запроса
    body = request.get_json()
    if not body or not body["login"] or not body["password"]:
        return jsonify({'message': 'Вы не передали логин и пароль!'}),401

    login = body["login"]
    password = body["password"]

    if login in USERS and USERS[login] == password:
        # Если логин и пароль найден в нашем словаре USERS, значит создаем токен
        token = jwt.encode({
            'login': login, #это payload, можно хранить, что угодно
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)
        },SECRET_KEY, algorithm='HS256')

        return jsonify({
            "message":"Успешная авторизация",
            "token": token
        }),200
    else:
        return jsonify({'message': 'Неверные учетные данные!'}),401

@app.route("/verify",methods=["POST"])
@token_required
def verify_token(login):
    return jsonify({
        "message":"Токен валиден",
        "login":login
    }),200

@app.route("/health", methods=["GET"])
def health():
    # Можно добавить любую логику для проверки и получения статуса
    return jsonify({"status":"success"}),200

if __name__ == "__main__":
    app.run(debug=False,port=5001,host="0.0.0.0")