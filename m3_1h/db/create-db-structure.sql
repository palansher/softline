CREATE TABLE IF NOT EXISTS catalogue(
       id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
       title varchar(50),
       brand varchar(30),
       short_info varchar(100),
       full_info text,
       price numeric,
       image_path varchar(100)
);

INSERT INTO catalogue (brand, title, price, short_info, full_info, image_path)
VALUES 
(
    'Porsche', 

    '911 Carrera', 

    14500000, 

    'Легендарный спортивный автомобиль с непревзойденной управляемостью.', 
    $$Porsche 911 Carrera — это культовый немецкий спортивный автомобиль с легендарной заднемоторной компоновкой, выпускаемый компанией Porsche.
    
Модель 911 отличается узнаваемым силуэтом, непревзойденной динамикой и 3,0-литровым оппозитным турбомотором, выдающим от 385 до 480 л.с. в зависимости от модификации (Carrera, T или S)$$,

    'img/cards/porsche.jpg'
),

(
    'BMW', 

    'M5 Competition', 

    12000000, 

    'Заряженный бизнес-седан, сочетающий в себе роскошь комфорта и ярость гоночного трека.', 
$$BMW M5 Competition — это экстремальная, более мощная и трековая модификация легендарного полноразмерного спортивного седана бизнес-класса, сочетающая в себе роскошь гражданского автомобиля и динамику суперкара.

Традиционно пакет Competition означает увеличенную мощность, перенастроенную жесткую подвеску и эксклюзивный темный декор кузова.
$$,

    'img/cards/porsche.jpg'
)

;

select * FROM catalogue \x\g

;

