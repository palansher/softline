# Импорт модуля Flask для создания веб-приложения
from flask import Flask, request, jsonify

# Импорт функции для загрузки переменных окружения из файла .env
from dotenv import load_dotenv

# Импорт библиотеки для работы с JWT токенами
import jwt

# Импорт модуля для работы с датой и временем
import datetime

# Импорт модуля для работы с переменными окружения операционной системы
import os

# Импорт декоратора wraps для сохранения метаданных функций
from functools import wraps

# Загрузка переменных окружения из файла .env
load_dotenv()

# Создание экземпляра Flask приложения
app = Flask(__name__)

# Получение секретного ключа из переменной окружения JWT_SECRET
SECRET_KEY = os.getenv('JWT_SECRET')

# Проверка: если секретный ключ не установлен, используем значение по умолчанию
if not SECRET_KEY:
    SECRET_KEY = "default_secret_key_for_docker_testing"

# Словарь с демо-пользователями для тестирования
USERS = {
    "admin": "admin123",
    "user": "user123"
}

# Декоратор для проверки валидности JWT токена
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Токен отсутствует!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Токен истёк!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Неверный токен!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Маршрут для логина
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Необходимо указать username и password'}), 400

    username = data['username']
    password = data['password']

    if username in USERS and USERS[username] == password:
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({
            'message': 'Успешная авторизация',
            'token': token,
            'expires_in': 3600
        }), 200
    else:
        return jsonify({'message': 'Неверные учетные данные'}), 401

# Маршрут для проверки токена
@app.route('/verify', methods=['POST'])
@token_required
def verify_token(current_user):
    return jsonify({
        'message': 'Токен валиден',
        'user': current_user
    }), 200

# Маршрут для health check (нужен для Docker)
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

# Точка входа приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)