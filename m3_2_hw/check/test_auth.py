"""
Проверка соответствия хэша текстовому паролю.
"""

# должен вернуть true, если хэш соответствует паролю, и false в противном случае.

from werkzeug.security import check_password_hash

# Хэш
db_hash = "scrypt:32768:8:1$aes6Ee07axzzOWJJ$46d6ef7204e8ae08bf0ec187fe444ba8391648176daa546e5b370c64aa335b36647ba88455fa8957f211ed3c0b360e6e45c49f1d01d2baf6cf8acd0a186eb798"

# Пароль
entered_password = "admin"

# Изолированная проверка библиотеки
is_valid = check_password_hash(db_hash, entered_password)
print(f"Библиотека werkzeug сопоставляет хэш и пароль? -> {is_valid}")
