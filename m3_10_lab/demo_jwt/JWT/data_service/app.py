# Импорт модуля Flask для создания веб-приложения
from flask import Flask, request, jsonify

# Импорт функции для загрузки переменных окружения из файла .env
from dotenv import load_dotenv

# Импорт библиотеки для работы с JWT токенами
import jwt

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

# Маршрут для получения защищённых данных
@app.route('/protected-data', methods=['GET'])
@token_required
def get_protected_data(current_user):
    return jsonify({
        'message': 'Доступ разрешён',
        'user': current_user,
        'data': {
            'secret_info': 'Это защищённые данные',
            'timestamp': '2024-01-01T12:00:00Z'
        }
    }), 200

# Маршрут только для администраторов
@app.route('/admin-only', methods=['GET'])
@token_required
def admin_only(current_user):
    if current_user != 'admin':
        return jsonify({'message': 'Доступ запрещён. Требуется роль администратора'}), 403
    return jsonify({
        'message': 'Доступ администратора разрешён',
        'admin_data': {
            'users_count': 100,
            'system_status': 'operational'
        }
    }), 200

# Маршрут для health check (нужен для Docker)
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

# Точка входа приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)