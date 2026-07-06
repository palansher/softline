-- Удаляем старые таблицы, если они были (строго в таком порядке!)
DROP TABLE IF EXISTS catalog;

DROP TABLE IF EXISTS brand;

CREATE TABLE IF NOT EXISTS brand(
        -- id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        id integer PRIMARY KEY, -- ID под вашим контролем
        name varchar(100) NOT NULL UNIQUE -- Название бренда не должно быть пустым и повторяться
);

CREATE TABLE IF NOT EXISTS catalog(
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
        image_big_path varchar(255), -- Объявляем внешний ключ
        CONSTRAINT fk_catalog_brand FOREIGN KEY (brand_id) REFERENCES brand(id) ON DELETE RESTRICT -- Не даст удалить бренд, если в каталоге есть его машины
);


/*
-- Очищаем зависимую таблицу catalog и сбрасываем счетчик ID
-- TRUNCATE TABLE catalog RESTART IDENTITY;
-- Если нужно очистить обе таблицы разом (учитывая связи Foreign Key)
-- TRUNCATE TABLE catalog, brand RESTART IDENTITY;
-- DELETE FROM catalog;
 */
-- Заполняем таблицу брендов
INSERT INTO brand(
        id,
        name)
VALUES
        (
                7,
                'Mercedes-Benz'),
(
                2,
                'BMW'),
(
                1,
                'Porsche'),
(
                4,
                'Toyota'),
(
                3,
                'Audi'),
(
                5,
                'Honda'),
(
                6,
                'Ford')
ON CONFLICT (
        name)
-- Чтобы не было ошибок при повторном запуске:
        DO NOTHING;

-- Заполняем каталог автомобилей
-- Предполагаем, что Mercedes получил id=1, BMW id=2, Porsche id=3
INSERT INTO catalog(
        brand_id,
        model,
        short_info,
        full_info,
        price,
        year_produced,
        mileage,
        is_available,
        image_small_path,
        image_big_path)
VALUES
        (
                1,
                '911 Carrera',
                'Легендарный спортивный автомобиль с непревзойденной управляемостью и немецким качеством.',
                '',
                14500000.00,
                DEFAULT,
                0,
                TRUE,
                'porsche-911-carrera_small.jpg',
                'porsche-911-carrera_big.jpg'),
(
                2,
                'M5 Competition',
                'Заряженный бизнес-седан, сочетающий в себе роскошь комфорта и ярость гоночного трека.',
                '',
                12000000.00,
                2024,
                0,
                TRUE,
                'bmw-m5-competition_small.jpg',
                'bmw-m5-competition_big.jpg'),
(
                3,
                'E-Tron GT',
                'Полностью электрический гран-туризмо, будущее динамики и прогрессивного дизайна.',
                '',
                11800000.00,
                2025,
                0,
                TRUE,
                'audi-e-tron-gt_small.jpg',
                'audi-e-tron-gt_big.jpg'),
(
                4,
                'Cruiser 300',
                'Легендарный внедорожник, готовый к любым испытаниям в условиях абсолютного комфорта.',
                '',
                10500000.00,
                2026,
                0,
                TRUE,
                'toyota-cruiser300_small.jpg',
                'toyota-cruiser300_big.jpg'),
(
                5,
                'Civic Type R',
                'Горячий хэтчбек для истинных ценителей скорости и точного японского инжиниринга.',
                '',
                5500000.00,
                DEFAULT,
                0,
                TRUE,
                'honda-civic-type-r_small.jpg',
                'honda-civic-type-r_big.jpg'),
(
                6,
                'Mustang Mach 1',
                'Американская икона мускул-каров с мощным V8 и агрессивным характером.',
                '',
                7200000.00,
                DEFAULT,
                0,
                TRUE,
                'ford-mustang-mach-1_small.jpg',
                'ford-mustang-mach-1_big.jpg');

-- INSERT INTO catalog (
--         brand,
--         title,
--         price,
--         short_info,
--         full_info,
--         image_path
--     )
-- VALUES (
--         'Porsche',
--         '911 Carrera',
--         14500000,
--         'Легендарный спортивный автомобиль с непревзойденной управляемостью.',
--         $$Porsche 911 Carrera — это культовый немецкий спортивный автомобиль с легендарной заднемоторной компоновкой,
--         выпускаемый компанией Porsche.Модель 911 отличается узнаваемым силуэтом,
--         непревзойденной динамикой и 3,
--         0 - литровым оппозитным турбомотором,
--         выдающим от 385 до 480 л.с.в зависимости от модификации (Carrera, T или S) $$,
--         'img/cards/porsche.jpg'
--     ),
--     (
--         'BMW',
--         'M5 Competition',
--         12000000,
--         'Заряженный бизнес-седан, сочетающий в себе роскошь комфорта и ярость гоночного трека.',
--         $$BMW M5 Competition — это экстремальная,
--         более мощная и трековая модификация легендарного полноразмерного спортивного седана бизнес - класса,
--         сочетающая в себе роскошь гражданского автомобиля и динамику суперкара.Традиционно пакет Competition означает увеличенную мощность,
--         перенастроенную жесткую подвеску и эксклюзивный темный декор кузова.$$,
--         'img/cards/porsche.jpg'
--     );
SELECT
        *
FROM
        brand;

SELECT
        *
FROM
        catalog;

