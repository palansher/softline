-- ============================================================================
-- ИНИЦИАЛИЗАЦИЯ ИНТЕРНЕТ-МАГАЗИНА: КАТАЛОГ, ПОЛЬЗОВАТЕЛИ, КОРЗИНЫ И ЗАКАЗЫ
-- Выполняется внутри единого транзакционного блока
-- ============================================================================

BEGIN;

-- Удаление старых объектов (если они существовали)
DROP VIEW IF EXISTS v_catalog_display;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_statuses;
DROP TABLE IF EXISTS cart_items;
DROP TABLE IF EXISTS carts;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS catalog;
DROP TABLE IF EXISTS brand;

-- Структура каталога товаров (Автомобили) --

-- Таблица брендов
CREATE TABLE IF NOT EXISTS brand (
    id bigint PRIMARY KEY, -- ID под нашим контролем    
    name varchar(100) NOT NULL UNIQUE -- Название бренда не должно быть пустым и повторяться
);

-- Таблица каталога
CREATE TABLE IF NOT EXISTS catalog (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    brand_id bigint NOT NULL,
    model varchar(100) NOT NULL,
    short_info varchar(255),
    full_info text,
    price numeric(12, 2) NOT NULL,
    year_produced smallint NOT NULL DEFAULT EXTRACT(YEAR FROM CURRENT_DATE), -- Год выпуска
    mileage integer NOT NULL DEFAULT 0, -- Пробег (в км, по умолчанию 0 для новых)
    is_available boolean NOT NULL DEFAULT TRUE, -- Статус: в наличии / продано
    image_small_path varchar(255),
    image_big_path varchar(255),

    -- Не даст удалить бренд, если в каталоге есть его машины
    CONSTRAINT fk_catalog_brand FOREIGN KEY (brand_id) REFERENCES brand (id) ON DELETE RESTRICT
);

-- Структура пользователей, корзин и заказов --

-- таблица ролей
CREATE TABLE IF NOT EXISTS roles (
    id int PRIMARY KEY,
    name varchar(50) NOT NULL UNIQUE,       -- Например: 'admin', 'moderator', 'user'
    description text                        -- Описание, за что роль отвечает
);

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email varchar(255) NOT NULL UNIQUE,
    password_hash varchar(255) NOT NULL,
    full_name varchar(255) NOT NULL,
    phone varchar(25),
    address text,
    role_id int NOT NULL DEFAULT 0,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP,

    -- Не позволит удалить роль, если она назначена юзерам
    CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE RESTRICT
);

-- Корзина покупок
CREATE TABLE IF NOT EXISTS carts (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id bigint NOT NULL,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP,

    -- Если удалить юзера, его корзина сотрется сама
    CONSTRAINT fk_carts_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Товары в корзине
CREATE TABLE IF NOT EXISTS cart_items (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cart_id bigint NOT NULL,
    item_id bigint NOT NULL, -- Тип данных bigint в соответствии с catalog.id
    quantity int NOT NULL CHECK (quantity > 0),

    -- Ограничение: один и тот же товар не может дублироваться в одной корзине отдельной строкой
    CONSTRAINT uq_cart_item UNIQUE (cart_id, item_id),

    -- Внешние ключи
    CONSTRAINT fk_items_cart FOREIGN KEY (cart_id) REFERENCES carts (id) ON DELETE CASCADE,
    CONSTRAINT fk_items_catalog FOREIGN KEY (item_id) REFERENCES catalog (id) ON DELETE RESTRICT
);

-- Справочник статусов заказов
CREATE TABLE IF NOT EXISTS order_statuses (
    id int PRIMARY KEY,
    name varchar(50) NOT NULL UNIQUE
);

-- Таблица заказов (с учетом скидки)
CREATE TABLE IF NOT EXISTS orders (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id bigint NOT NULL,
    status int NOT NULL DEFAULT 0,

    -- Сумма к оплате (уже за вычетом скидки)
    total_amount numeric(10, 2) NOT NULL CHECK (total_amount >= 0),

    -- Сумма предоставленной скидки (по промокодам, акциям и т.д.)
    discount_amount numeric(10, 2) NOT NULL DEFAULT 0.00 CHECK (discount_amount >= 0),

    shipping_address text NOT NULL,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP,

    -- Ограничение на уровне таблицы: скидка не может быть больше, чем итоговая сумма
    CONSTRAINT chk_discount_limit CHECK (discount_amount <= total_amount),

    -- Внешние ключи
    CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE RESTRICT,
    CONSTRAINT fk_orders_status FOREIGN KEY (status) REFERENCES order_statuses (id) ON DELETE RESTRICT
);

-- Содержимое заказа
CREATE TABLE IF NOT EXISTS order_items (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id bigint NOT NULL,
    catalog_id bigint NOT NULL, -- Тип данных bigint в соответствии с catalog.id
    price numeric(10, 2) NOT NULL CHECK (price >= 0), -- Исходная цена товара на момент покупки
    quantity int NOT NULL CHECK (quantity > 0),

    CONSTRAINT uq_order_item UNIQUE (order_id, catalog_id),
    CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
    CONSTRAINT fk_items_catalog FOREIGN KEY (catalog_id) REFERENCES catalog (id) ON DELETE RESTRICT
);

-- Стандартные индексы (Создаются внутри транзакции без CONCURRENTLY) --

-- Индекс для быстрых JOIN и фильтрации по ролям
CREATE INDEX IF NOT EXISTS idx_users_role_id ON users (role_id); -- noqa: PG01

-- Индекс для быстрого поиска корзины конкретного пользователя
CREATE INDEX IF NOT EXISTS idx_carts_user_id ON carts (user_id); -- noqa: PG01

-- Индекс для быстрой сборки содержимого корзины
CREATE INDEX IF NOT EXISTS idx_cart_items_cart_id ON cart_items (cart_id); -- noqa: PG01

-- Индексы для таблицы заказов
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders (user_id); -- noqa: PG01
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders (status); -- noqa: PG01

-- Индекс для сборки состава чека/заказа
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items (order_id); -- noqa: PG01

-- Наполнение справочников и демонстрационных данных --

-- Заполняем таблицу брендов
INSERT INTO brand (id, name) VALUES
(7, 'Mercedes-Benz'),
(2, 'BMW'),
(1, 'Porsche'),
(4, 'Toyota'),
(3, 'Audi'),
(5, 'Honda'),
(6, 'Ford')
ON CONFLICT (name) DO NOTHING;

-- Заполняем каталог автомобилей
INSERT INTO catalog (brand_id, model, short_info, full_info, price, year_produced, mileage, is_available, image_small_path, image_big_path) VALUES
(
    1, '911 Carrera',
    'Легендарный спортивный автомобиль с непревзойденной управляемостью и немецким качеством.',
    $$Porsche 911 Carrera — это синоним чистокровного автомобильного спорта. Икона, бережно пронесшая свой силуэт сквозь десятилетия, предлагает бескомпромиссную динамику на грани возможностей.

Особенности комплектации:
• Оппозитный 3.0-литровый битурбо двигатель, выдающий мгновенный отклик.
• Молниеносная 8-ступенчатая трансмиссия PDK.
• Спортивная выхлопная система с регулировкой громкости клапанов.
• Премиальная аудиосистема Bose и салон из расширенной натуральной кожи Truffle Brown.

Этот автомобиль рожден для тех, кто не ищет компромиссов между повседневным комфортом и чистым адреналином гоночного трека.$$,
    14500000.00, DEFAULT, 0, TRUE, 'porsche-911-carrera_small.jpg', 'porsche-911-carrera_big.jpg'
),
(
    2, 'M5 Competition',
    'Заряженный бизнес-седан, сочетающий в себе роскошь комфорта и ярость гоночного трека.',
    $$BMW M5 Competition переписывает законы физики, offering динамику суперкара в кузове роскошного бизнес-седана. Это абсолютный флагман линейки M, созданный доминировать.

Ключевые преимущества:
• Двигатель V8 M TwinPower Turbo мощностью 625 л.с.
• Интеллектуальный полный привод M xDrive с возможностью полного отключения передней оси для классического заднеприводного дрифта.
• Адаптивная подвеска Competition, настроенная на Нюрбургринге.
• Карбон-керамическая тормозная система.

Салон Individual с мультиконтурными сиденьями, вентиляцией и массажем позволит наслаждаться дальними поездками, пока вы не решите нажать кнопку M-режима.$$,
    12000000.00, 2024, 0, TRUE, 'bmw-m5-competition_small.jpg', 'bmw-m5-competition_big.jpg'
),
(
    3, 'E-Tron GT',
    'Полностью электрический гран-туризмо, будущее динамики и прогрессивного дизайна.',
    $$Audi e-tron GT — это манифест прогрессивного видения будущего от инженеров из Ингольштадта. Настоящий Гран-Туризмо на электротяге, который приковывает к себе взгляды в любом потоке.

Технологическое превосходство:
• Двухмоторный полный привод quattro с мгновенным распределением крутящего момента.
• 800-вольтовая архитектура, обеспечивающая сверхбыструю зарядку до 80% всего за 22 минуты.
• Трехкамерная пневмоподвеска для максимальной плавности хода.
• Панорамная крыша и лазерная оптика Audi Laser Light.

Бесшумный, хищный и невероятно быстрый автомобиль для тех, кто опережает свое время.$$,
    11800000.00, 2025, 1000, TRUE, 'audi-e-tron-gt_small.jpg', 'audi-e-tron-gt_big.jpg'
),
(
    4, 'Cruiser 300',
    'Легендарный внедорожник, готовый к любым испытаниям в условиях абсолютного комфорта.',
    $$Toyota Land Cruiser 300 — флагман внедорожной линейки, унаследовавший легендарную надежность и получивший премиальный уровень исполнения. Ему не важен тип покрытия, важна лишь цель.

Превосходство на любых маршрутах:
• Новый мощный двигатель V6 с двойным турбонаддувом и 10-ступенчатый автомат.
• Модернизированная система кинетической стабилизации подвески E-KDSS.
• Роскошный 7-местный салон с четырехзонным климат-контролем и мониторами для задних пассажиров.
• Комплекс систем безопасности Toyota Safety Sense последнего поколения.

Бесупречный выбор для лидеров, привыкших контролировать любую ситуацию и ценить уверенность в каждом километре.$$,
    10500000.00, 2026, 0, TRUE, 'toyota-cruiser300_small.jpg', 'toyota-cruiser300_big.jpg'
),
(
    5, 'Civic Type R',
    'Горячий хэтчбек для истинных ценителей скорости и точного японского инжиниринга.',
    $$Honda Civic Type R — это чистокровное воплощение гоночной философии бренда. Перед вами один из самых быстрых и технологичных переднеприводных автомобилей планеты, готовый к трек-дням прямо из шоурума.

Анатомия скорости:
• Доработанный 2.0-литровый турбомотор VTEC с взрывным характером на высоких оборотах.
• Эталонная 6-ступенчатая механическая коробка передач с системой автоматической перегазовки.
• Дифференциал повышенного трения (LSD) для идеального зацепа в поворотах.
• Спортивные ковши багрово-красного цвета и эксклюзивный цифровой телеметрийный комплекс LogR.

Это автомобиль с характером, который дарит честные, механические эмоции от управления.$$,
    5500000.00, DEFAULT, 0, TRUE, 'honda-civic-type-r_small.jpg', 'honda-civic-type-r_big.jpg'
),
(
    6, 'Mustang Mach 1',
    'Американская икона мускул-каров с мощным V8 и агрессивным характером.',
    $$Ford Mustang Mach 1 — это лимитированная серия, созданная на стыке классической культуры масл-каров и современных трековых технологий. Под капотом бьется настоящее американское сердце.

Легендарная инженерия:
• Атмосферный V8 Coyote 5.0 мощностью 480 л.с., издающий сочный, ни с чем не сравнимый рык.
• Компоненты охлаждения и подвески, позаимствованные у гоночных версий Shelby.
• Уникальный аэродинамический обвес Mach 1, увеличивающий прижимную силу на высоких скоростях.
• Спортивная выхлопная система с активными клапанами.

Мужской характер, бешеная харизма и бескомпромиссная мощь заднего привода для ценителей настоящей классики.$$,
    7200000.00, DEFAULT, 0, TRUE, 'ford-mustang-mach-1_small.jpg', 'ford-mustang-mach-1_big.jpg'
);

-- Вставляем фиксированные значения ролей
INSERT INTO roles (id, name, description) VALUES
(0, 'user', 'Обычный зарегистрированный пользователь'),
(1, 'admin', 'Администратор системы'),
(2, 'moderator', 'Модератор контента')
ON CONFLICT (id) DO NOTHING;

-- Добавляем первого администратора системы (ID сгенерируется автоматически)
/*
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('ваш_пароль'))"
*/
INSERT INTO users (email, password_hash, full_name, phone, address, role_id) VALUES
(
    'admin@shop.com',
    -- Демонстрационный хэш пароля (admin)
    'scrypt:32768:8:1$aes6Ee07axzzOWJJ$46d6ef7204e8ae08bf0ec187fe444ba8391648176daa546e5b370c64aa335b36647ba88455fa8957f211ed3c0b360e6e45c49f1d01d2baf6cf8acd0a186eb798',
    'Главный Администратор',
    '+7 (999) 111-22-33',
    'Приют для бездомных людей при храме Свв. мцц. Веры, Надежды, Любови и матери их Софии, г. Ожерелье , Московская область, Каширский район, г. Ожерелье, 1-я Больничная улица, д.2',
    1 -- Ссылка на роль 'admin' (id = 1)
)
ON CONFLICT (email) DO NOTHING;

-- Наполнение статусами заказов
INSERT INTO order_statuses (id, name) VALUES
(0, 'создан'),
(1, 'оплачен'),
(2, 'доставлен'),
(3, 'отменен')
ON CONFLICT (id) DO NOTHING;

-- Представления (Views) --

CREATE OR REPLACE VIEW v_catalog_display AS
SELECT
    c.id AS car_id,
    b.name AS brand_name,
    c.model AS model_name,
    c.short_info,
    c.full_info,
    c.price,
    c.year_produced,
    c.mileage,
    c.image_small_path,
    c.image_big_path
FROM
    catalog AS c
INNER JOIN brand AS b ON c.brand_id = b.id
WHERE
    c.is_available = TRUE;

COMMIT;

-- Контрольная проверка созданных данных --

SELECT * FROM brand;
SELECT * FROM catalog;
SELECT * FROM users;
