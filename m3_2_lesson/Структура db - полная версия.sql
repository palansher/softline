-- 1. Пользователи
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Товары
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

-- 3. Корзины (несколько корзин на пользователя)
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,        -- связь с users.id (логическая)
    name VARCHAR(100) DEFAULT 'Моя корзина',
    status VARCHAR(20) DEFAULT 'active',  -- active, saved
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Товары в корзине
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INT NOT NULL,         -- связь с carts.id (логическая)
    item_id INT NOT NULL,         -- связь с items.id (логическая)
    quantity INT NOT NULL CHECK (quantity > 0)
);

-- 5. Заказы
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,         -- связь с users.id (логическая)
    cart_id INT NOT NULL,         -- связь с carts.id (логическая)
    order_status VARCHAR(30) DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Товары в заказе (слепок цен на момент покупки)
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,        -- связь с orders.id (логическая)
    item_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL
);
