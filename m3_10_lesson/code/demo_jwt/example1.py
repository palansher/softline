import jwt
import secrets

# Создаем безопасный ключ (32 байта - 256 бит)

SECRET_KEY = secrets.token_urlsafe(32)
print(f"Секретный ключ: {SECRET_KEY}")
print(f"Длина ключа: {len(SECRET_KEY)}")

# Кодируем и декодируем данные одним ключом
encoded = jwt.encode({'role':'admin'}, SECRET_KEY, algorithm='HS256')
print(f'jwt токен: {encoded}')

decoded = jwt.decode(encoded, SECRET_KEY, algorithms=['HS256'])
print(f'В JWT была информация: {decoded}')