CREATE TABLE IF NOT EXISTS brand (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE -- Название бренда не должно быть пустым и повторяться
);

CREATE TABLE IF NOT EXISTS catalog (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    brand_id bigint NOT NULL, 
    title varchar(100) NOT NULL,
    short_info varchar(255),
    full_info text,
    price numeric(12, 2) NOT NULL,
    year_produced smallint NOT NULL,          -- Год выпуска
    mileage integer NOT NULL DEFAULT 0,       -- Пробег (в км, по умолчанию 0 для новых)
    is_available boolean NOT NULL DEFAULT true, -- Статус: в наличии / продано
    image_small_path varchar(255),
    image_big_path varchar(255),

    -- Объявляем внешний ключ
    CONSTRAINT fk_catalog_brand 
        FOREIGN KEY (brand_id) 
        REFERENCES brand(id) 
        ON DELETE RESTRICT -- Не даст удалить бренд, если в каталоге есть его машины
);


-- 1. Заполняем таблицу брендов
INSERT INTO brand (name) VALUES 
('Mercedes-Benz'),
('BMW'),
('Porsche')
ON CONFLICT (name) DO NOTHING; -- Чтобы не было ошибок при повторном запуске

INSERT INTO catalog (
        brand,
        title,
        price,
        short_info,
        full_info,
        image_path
    )
VALUES (
        'Porsche',
        '911 Carrera',
        14500000,
        'Легендарный спортивный автомобиль с непревзойденной управляемостью.',
        $$Porsche 911 Carrera — это культовый немецкий спортивный автомобиль с легендарной заднемоторной компоновкой,
        выпускаемый компанией Porsche.Модель 911 отличается узнаваемым силуэтом,
        непревзойденной динамикой и 3,
        0 - литровым оппозитным турбомотором,
        выдающим от 385 до 480 л.с.в зависимости от модификации (Carrera, T или S) $$,
        'img/cards/porsche.jpg'
    ),
    (
        'BMW',
        'M5 Competition',
        12000000,
        'Заряженный бизнес-седан, сочетающий в себе роскошь комфорта и ярость гоночного трека.',
        $$BMW M5 Competition — это экстремальная,
        более мощная и трековая модификация легендарного полноразмерного спортивного седана бизнес - класса,
        сочетающая в себе роскошь гражданского автомобиля и динамику суперкара.Традиционно пакет Competition означает увеличенную мощность,
        перенастроенную жесткую подвеску и эксклюзивный темный декор кузова.$$,
        'img/cards/porsche.jpg'
    );
select *
FROM catalogue \ x \ g;