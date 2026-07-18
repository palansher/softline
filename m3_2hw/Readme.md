# Выполнение ДЗ 3.2

## Регистрация пользователя

### демо покупатель

palansher@outlook.com
qwerty

### Демо продавец

admin@shop.com
admin

### Хеширование паролей

Flask использует встроенный метод scrypt из библиотеки werkzeug.security. Хэш выглядит как scrypt:32768:8:1$....
Метод check_password_hash() из werkzeug не понимает хэши bcrypt по умолчанию.

```sql
-- Добавляем первого администратора системы (ID сгенерируется автоматически)
INSERT INTO users (email, password_hash, full_name, phone, address, role_id) VALUES
(
    'admin@shop.com',
    -- Валидный scrypt-хэш от werkzeug.security для пароля "admin"
    'scrypt:32768:8:1$aes6Ee07axzzOWJJ$46d6ef7204e8ae08bf0ec187fe444ba8391648176daa546e5b370c64aa335b36647ba88455fa8957f211ed3c0b360e6e45c49f1d01d2baf6cf8acd0a186eb798',
    'Главный Администратор',
    '+7 (999) 111-22-33',
    'Центральный office',
    1 -- Ссылка на роль 'admin' (id = 1)
)
ON CONFLICT (email) DO NOTHING;
```

### Ручное обновление пароля

нужно вставить хэш формата scrypt, сгенерированный самой библиотекой werkzeug.security

`python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('ваш_пароль'))"`

Ручное обновление существующей записи админа (UPSERT)

```sql
/* SQL-запрос, который либо вставит админа (если его нет), либо полностью обновит его пароль и данные (если его email admin@shop.com уже занят) */
INSERT INTO users (email, password_hash, full_name, phone, address, role_id) 
VALUES
(
    'admin@shop.com',
    -- хэш для 'admin':
    'scrypt:32768:8:1$aes6Ee07axzzOWJJ$46d6ef7204e8ae08bf0ec187fe444ba8391648176daa546e5b370c64aa335b36647ba88455fa8957f211ed3c0b360e6e45c49f1d01d2baf6cf8acd0a186eb798', 
    'Главный Администратор',
    '+7 (999) 111-22-33',
    'Приют для бездомных людей при храме Свв. мцц. Веры, Надежды, Любови и матери их Софии, г. Ожерелье , Московская область, Каширский район, г. Ожерелье, 1-я Больничная улица, д.2',
    1
)
ON CONFLICT (email) 
DO UPDATE SET 
    password_hash = EXCLUDED.password_hash,
    full_name     = EXCLUDED.full_name,
    phone         = EXCLUDED.phone,
    address       = EXCLUDED.address,
    role_id       = EXCLUDED.role_id;    
```

<!-- `pip install psycopg2` -->
