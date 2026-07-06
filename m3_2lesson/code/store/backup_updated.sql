CREATE TABLE item(
       item_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
       title varchar(30),
       price numeric,
       info text,
       photo varchar(100)
);

CREATE TABLE cart(
   id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
   item_id bigint,
   quantity smallint
);

INSERT INTO item(title,price,info,photo) VALUES
         ('Audi',1000,'В наличии','audi.jpg'),
         ('BMW',1300,'Под заказ','bmw.jpg'),
         ('VW',900,'В наличии','vw.jpg'),
         ('Skoda',950,'В наличии','skoda.jpg');
        
select * FROM item         