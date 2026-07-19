--
-- PostgreSQL database dump
--

\restrict Lg7VRFGuGbpi1SHRjzLaj94f7SWLUQFLmDOP3ZHIbH3KyeUn4rbS0TkycVwh5cq

-- Dumped from database version 18.4 (Debian 18.4-1.pgdg13+1)
-- Dumped by pg_dump version 18.4 (Debian 18.4-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: shop_admin
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO shop_admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: brand; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.brand (
    id bigint NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.brand OWNER TO postgres;

--
-- Name: cart_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart_items (
    id bigint NOT NULL,
    cart_id bigint NOT NULL,
    item_id bigint NOT NULL,
    quantity integer NOT NULL,
    CONSTRAINT cart_items_quantity_check CHECK ((quantity > 0))
);


ALTER TABLE public.cart_items OWNER TO postgres;

--
-- Name: cart_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.cart_items ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.cart_items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: carts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.carts (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.carts OWNER TO postgres;

--
-- Name: carts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.carts ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.carts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: catalog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalog (
    id bigint NOT NULL,
    brand_id bigint NOT NULL,
    model character varying(100) NOT NULL,
    short_info character varying(255),
    full_info text,
    price numeric(12,2) NOT NULL,
    year_produced smallint DEFAULT EXTRACT(year FROM CURRENT_DATE) NOT NULL,
    mileage integer DEFAULT 0 NOT NULL,
    is_available boolean DEFAULT true NOT NULL,
    image_small_path character varying(255),
    image_big_path character varying(255)
);


ALTER TABLE public.catalog OWNER TO postgres;

--
-- Name: catalog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.catalog ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.catalog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    id bigint NOT NULL,
    order_id bigint NOT NULL,
    catalog_id bigint NOT NULL,
    price numeric(10,2) NOT NULL,
    quantity integer NOT NULL,
    CONSTRAINT order_items_price_check CHECK ((price >= (0)::numeric)),
    CONSTRAINT order_items_quantity_check CHECK ((quantity > 0))
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.order_items ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.order_items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: order_statuses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_statuses (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.order_statuses OWNER TO postgres;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    status integer DEFAULT 0 NOT NULL,
    total_amount numeric(10,2) NOT NULL,
    discount_amount numeric(10,2) DEFAULT 0.00 NOT NULL,
    shipping_address text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_discount_limit CHECK ((discount_amount <= total_amount)),
    CONSTRAINT orders_discount_amount_check CHECK ((discount_amount >= (0)::numeric)),
    CONSTRAINT orders_total_amount_check CHECK ((total_amount >= (0)::numeric))
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.orders ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.orders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    full_name character varying(255) NOT NULL,
    phone character varying(25),
    address text,
    role_id integer DEFAULT 0 NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.users ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: v_catalog_display; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_catalog_display AS
 SELECT c.id AS car_id,
    b.name AS brand_name,
    c.model AS model_name,
    c.short_info,
    c.full_info,
    c.price,
    c.year_produced,
    c.mileage,
    c.image_small_path,
    c.image_big_path
   FROM (public.catalog c
     JOIN public.brand b ON ((c.brand_id = b.id)))
  WHERE (c.is_available = true);


ALTER VIEW public.v_catalog_display OWNER TO postgres;

--
-- Data for Name: brand; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.brand VALUES (7, 'Mercedes-Benz');
INSERT INTO public.brand VALUES (2, 'BMW');
INSERT INTO public.brand VALUES (1, 'Porsche');
INSERT INTO public.brand VALUES (4, 'Toyota');
INSERT INTO public.brand VALUES (3, 'Audi');
INSERT INTO public.brand VALUES (5, 'Honda');
INSERT INTO public.brand VALUES (6, 'Ford');


--
-- Data for Name: cart_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cart_items OVERRIDING SYSTEM VALUE VALUES (10, 1, 2, 1);


--
-- Data for Name: carts; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.carts OVERRIDING SYSTEM VALUE VALUES (1, 2, '2026-07-18 19:31:49.434294+00');
INSERT INTO public.carts OVERRIDING SYSTEM VALUE VALUES (2, 1, '2026-07-18 21:33:52.662757+00');
INSERT INTO public.carts OVERRIDING SYSTEM VALUE VALUES (3, 5, '2026-07-19 00:43:31.753851+00');


--
-- Data for Name: catalog; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.catalog OVERRIDING SYSTEM VALUE VALUES (1, 1, '911 Carrera', 'Легендарный спортивный автомобиль с непревзойденной управляемостью и немецким качеством.', 'Porsche 911 Carrera — это синоним чистокровного автомобильного спорта. Икона, бережно пронесшая свой силуэт сквозь десятилетия, предлагает бескомпромиссную динамику на грани возможностей.

Особенности комплектации:
• Оппозитный 3.0-литровый битурбо двигатель, выдающий мгновенный отклик.
• Молниеносная 8-ступенчатая трансмиссия PDK.
• Спортивная выхлопная система с регулировкой громкости клапанов.
• Премиальная аудиосистема Bose и салон из расширенной натуральной кожи Truffle Brown.

Этот автомобиль рожден для тех, кто не ищет компромиссов между повседневным комфортом и чистым адреналином гоночного трека.', 14500000.00, 2026, 0, true, 'porsche-911-carrera_small.jpg', 'porsche-911-carrera_big.jpg');
INSERT INTO public.catalog OVERRIDING SYSTEM VALUE VALUES (2, 2, 'M5 Competition', 'Заряженный бизнес-седан, сочетающий в себе роскошь комфорта и ярость гоночного трека.', 'BMW M5 Competition переписывает законы физики, offering динамику суперкара в кузове роскошного бизнес-седана. Это абсолютный флагман линейки M, созданный доминировать.

Ключевые преимущества:
• Двигатель V8 M TwinPower Turbo мощностью 625 л.с.
• Интеллектуальный полный привод M xDrive с возможностью полного отключения передней оси для классического заднеприводного дрифта.
• Адаптивная подвеска Competition, настроенная на Нюрбургринге.
• Карбон-керамическая тормозная система.

Салон Individual с мультиконтурными сиденьями, вентиляцией и массажем позволит наслаждаться дальними поездками, пока вы не решите нажать кнопку M-режима.', 12000000.00, 2024, 0, true, 'bmw-m5-competition_small.jpg', 'bmw-m5-competition_big.jpg');
INSERT INTO public.catalog OVERRIDING SYSTEM VALUE VALUES (3, 3, 'E-Tron GT', 'Полностью электрический гран-туризмо, будущее динамики и прогрессивного дизайна.', 'Audi e-tron GT — это манифест прогрессивного видения будущего от инженеров из Ингольштадта. Настоящий Гран-Туризмо на электротяге, который приковывает к себе взгляды в любом потоке.

Технологическое превосходство:
• Двухмоторный полный привод quattro с мгновенным распределением крутящего момента.
• 800-вольтовая архитектура, обеспечивающая сверхбыструю зарядку до 80% всего за 22 минуты.
• Трехкамерная пневмоподвеска для максимальной плавности хода.
• Панорамная крыша и лазерная оптика Audi Laser Light.

Бесшумный, хищный и невероятно быстрый автомобиль для тех, кто опережает свое время.', 11800000.00, 2025, 1000, true, 'audi-e-tron-gt_small.jpg', 'audi-e-tron-gt_big.jpg');
INSERT INTO public.catalog OVERRIDING SYSTEM VALUE VALUES (4, 4, 'Cruiser 300', 'Легендарный внедорожник, готовый к любым испытаниям в условиях абсолютного комфорта.', 'Toyota Land Cruiser 300 — флагман внедорожной линейки, унаследовавший легендарную надежность и получивший премиальный уровень исполнения. Ему не важен тип покрытия, важна лишь цель.

Превосходство на любых маршрутах:
• Новый мощный двигатель V6 с двойным турбонаддувом и 10-ступенчатый автомат.
• Модернизированная система кинетической стабилизации подвески E-KDSS.
• Роскошный 7-местный салон с четырехзонным климат-контролем и мониторами для задних пассажиров.
• Комплекс систем безопасности Toyota Safety Sense последнего поколения.

Бесупречный выбор для лидеров, привыкших контролировать любую ситуацию и ценить уверенность в каждом километре.', 10500000.00, 2026, 0, true, 'toyota-cruiser300_small.jpg', 'toyota-cruiser300_big.jpg');
INSERT INTO public.catalog OVERRIDING SYSTEM VALUE VALUES (5, 5, 'Civic Type R', 'Горячий хэтчбек для истинных ценителей скорости и точного японского инжиниринга.', 'Honda Civic Type R — это чистокровное воплощение гоночной философии бренда. Перед вами один из самых быстрых и технологичных переднеприводных автомобилей планеты, готовый к трек-дням прямо из шоурума.

Анатомия скорости:
• Доработанный 2.0-литровый турбомотор VTEC с взрывным характером на высоких оборотах.
• Эталонная 6-ступенчатая механическая коробка передач с системой автоматической перегазовки.
• Дифференциал повышенного трения (LSD) для идеального зацепа в поворотах.
• Спортивные ковши багрово-красного цвета и эксклюзивный цифровой телеметрийный комплекс LogR.

Это автомобиль с характером, который дарит честные, механические эмоции от управления.', 5500000.00, 2026, 0, true, 'honda-civic-type-r_small.jpg', 'honda-civic-type-r_big.jpg');
INSERT INTO public.catalog OVERRIDING SYSTEM VALUE VALUES (6, 6, 'Mustang Mach 1', 'Американская икона мускул-каров с мощным V8 и агрессивным характером.', 'Ford Mustang Mach 1 — это лимитированная серия, созданная на стыке классической культуры масл-каров и современных трековых технологий. Под капотом бьется настоящее американское сердце.

Легендарная инженерия:
• Атмосферный V8 Coyote 5.0 мощностью 480 л.с., издающий сочный, ни с чем не сравнимый рык.
• Компоненты охлаждения и подвески, позаимствованные у гоночных версий Shelby.
• Уникальный аэродинамический обвес Mach 1, увеличивающий прижимную силу на высоких скоростях.
• Спортивная выхлопная система с активными клапанами.

Мужской характер, бешеная харизма и бескомпромиссная мощь заднего привода для ценителей настоящей классики.', 7200000.00, 2026, 0, true, 'ford-mustang-mach-1_small.jpg', 'ford-mustang-mach-1_big.jpg');


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.order_items OVERRIDING SYSTEM VALUE VALUES (1, 1, 2, 12000000.00, 2);
INSERT INTO public.order_items OVERRIDING SYSTEM VALUE VALUES (2, 1, 5, 5500000.00, 3);
INSERT INTO public.order_items OVERRIDING SYSTEM VALUE VALUES (3, 2, 2, 12000000.00, 3);
INSERT INTO public.order_items OVERRIDING SYSTEM VALUE VALUES (4, 2, 3, 11800000.00, 1);
INSERT INTO public.order_items OVERRIDING SYSTEM VALUE VALUES (5, 3, 3, 11800000.00, 1);


--
-- Data for Name: order_statuses; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.order_statuses VALUES (0, 'создан');
INSERT INTO public.order_statuses VALUES (1, 'оплачен');
INSERT INTO public.order_statuses VALUES (2, 'доставлен');
INSERT INTO public.order_statuses VALUES (3, 'отменен');


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.orders OVERRIDING SYSTEM VALUE VALUES (1, 2, 0, 40500000.00, 0.00, 'Москва, Кремль, д. 1', '2026-07-18 23:00:19.76912+00');
INSERT INTO public.orders OVERRIDING SYSTEM VALUE VALUES (2, 5, 0, 47800000.00, 0.00, 'на деревню дедушке', '2026-07-19 00:44:57.635213+00');
INSERT INTO public.orders OVERRIDING SYSTEM VALUE VALUES (3, 1, 0, 11800000.00, 0.00, 'Приют для бездомных людей при храме Свв. мцц. Веры, Надежды, Любови и матери их Софии, г. Ожерелье , Московская область, Каширский район, г. Ожерелье, 1-я Больничная улица, д.2', '2026-07-19 02:50:29.075098+00');


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.roles VALUES (0, 'user', 'Обычный зарегистрированный пользователь');
INSERT INTO public.roles VALUES (1, 'admin', 'Администратор системы');
INSERT INTO public.roles VALUES (2, 'moderator', 'Модератор контента');


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users OVERRIDING SYSTEM VALUE VALUES (2, 'palansher@outlook.com', 'scrypt:32768:8:1$ha0iK3ZjkzWb6rbH$2c9dd650b0b7fb4fdacfef71d554517ac14728712be734b12a815f926047117f73f815b24f6f7dae6dd9e6c7f3f7d9de31e28bf1dba9fd3d22f53092ff1fcd70', 'Перепеченко Владимир Александрович', '+79168387021', 'Москва, Кремль, д. 1', 0, '2026-07-18 19:31:49.434294+00');
INSERT INTO public.users OVERRIDING SYSTEM VALUE VALUES (1, 'admin@shop.com', 'scrypt:32768:8:1$aes6Ee07axzzOWJJ$46d6ef7204e8ae08bf0ec187fe444ba8391648176daa546e5b370c64aa335b36647ba88455fa8957f211ed3c0b360e6e45c49f1d01d2baf6cf8acd0a186eb798', 'Главный Администратор', '+7 (999) 111-22-33', 'Приют для бездомных людей при храме Свв. мцц. Веры, Надежды, Любови и матери их Софии, г. Ожерелье , Московская область, Каширский район, г. Ожерелье, 1-я Больничная улица, д.2', 1, '2026-07-18 19:18:26.563904+00');
INSERT INTO public.users OVERRIDING SYSTEM VALUE VALUES (5, 'ivanov@mail.ru', 'scrypt:32768:8:1$5kvjpxrejF7JEsB9$0ab5ad4a47df5dd5a724da527787ad3442a0b451e28802d7a297eed75cbd153cf6aa1ee7a7fe5b46d5dbebb9e47d1c8efa7f3d247c24f8dde20688fcbba9c769', 'Иванов Иван', '+79568745', 'на деревню дедушке', 0, '2026-07-19 00:43:31.753851+00');


--
-- Name: cart_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cart_items_id_seq', 10, true);


--
-- Name: carts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.carts_id_seq', 3, true);


--
-- Name: catalog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.catalog_id_seq', 6, true);


--
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_items_id_seq', 5, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: brand brand_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.brand
    ADD CONSTRAINT brand_name_key UNIQUE (name);


--
-- Name: brand brand_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.brand
    ADD CONSTRAINT brand_pkey PRIMARY KEY (id);


--
-- Name: cart_items cart_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);


--
-- Name: carts carts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_pkey PRIMARY KEY (id);


--
-- Name: catalog catalog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog
    ADD CONSTRAINT catalog_pkey PRIMARY KEY (id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: order_statuses order_statuses_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_statuses
    ADD CONSTRAINT order_statuses_name_key UNIQUE (name);


--
-- Name: order_statuses order_statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_statuses
    ADD CONSTRAINT order_statuses_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: cart_items uq_cart_item; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT uq_cart_item UNIQUE (cart_id, item_id);


--
-- Name: order_items uq_order_item; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT uq_order_item UNIQUE (order_id, catalog_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: idx_cart_items_cart_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cart_items_cart_id ON public.cart_items USING btree (cart_id);


--
-- Name: idx_carts_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_carts_user_id ON public.carts USING btree (user_id);


--
-- Name: idx_order_items_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_order_items_order_id ON public.order_items USING btree (order_id);


--
-- Name: idx_orders_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_orders_status ON public.orders USING btree (status);


--
-- Name: idx_orders_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_orders_user_id ON public.orders USING btree (user_id);


--
-- Name: idx_users_role_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_role_id ON public.users USING btree (role_id);


--
-- Name: carts fk_carts_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT fk_carts_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: catalog fk_catalog_brand; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog
    ADD CONSTRAINT fk_catalog_brand FOREIGN KEY (brand_id) REFERENCES public.brand(id) ON DELETE RESTRICT;


--
-- Name: cart_items fk_items_cart; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT fk_items_cart FOREIGN KEY (cart_id) REFERENCES public.carts(id) ON DELETE CASCADE;


--
-- Name: cart_items fk_items_catalog; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT fk_items_catalog FOREIGN KEY (item_id) REFERENCES public.catalog(id) ON DELETE RESTRICT;


--
-- Name: order_items fk_items_catalog; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_items_catalog FOREIGN KEY (catalog_id) REFERENCES public.catalog(id) ON DELETE RESTRICT;


--
-- Name: order_items fk_items_order; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- Name: orders fk_orders_status; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_orders_status FOREIGN KEY (status) REFERENCES public.order_statuses(id) ON DELETE RESTRICT;


--
-- Name: orders fk_orders_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: users fk_users_role; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict Lg7VRFGuGbpi1SHRjzLaj94f7SWLUQFLmDOP3ZHIbH3KyeUn4rbS0TkycVwh5cq

