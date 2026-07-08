--
-- PostgreSQL database dump
--

\restrict rtc6O5GAHbimrFm5neiA4PmsW9Pc4kgr2bm0Fu22Eu6ARKmoydTTRae4BAhRg3l

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: stock; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stock (
    id integer NOT NULL,
    name character varying NOT NULL,
    price integer DEFAULT 0 NOT NULL,
    discount integer DEFAULT 0 NOT NULL,
    property_1 character varying,
    property_2 character varying,
    property_3 character varying,
    property_4 character varying,
    foto character varying
);


ALTER TABLE public.stock OWNER TO postgres;

--
-- Name: TABLE stock; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.stock IS 'Магазин';


--
-- Name: stock_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.stock ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.stock_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: stock; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stock (id, name, price, discount, property_1, property_2, property_3, property_4, foto) FROM stdin;
2	Тормоза	1500	0	Дисковые	Brembpo	-	-	break.jpg
3	Аккумулятор	9000	0	Емкость 64	12В	Zubr	-	battery.jpg
4	Фильтр масляный	2000	0	Вставка	Bosch	-	-	filter.jpg
1	oil	1000	50	Вязкость: 5w-40	Синтетика	Производитель:Shell	Емкость:4л	oil.jpg
\.


--
-- Name: stock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stock_id_seq', 4, true);


--
-- Name: TABLE stock; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE public.stock TO webstore;


--
-- PostgreSQL database dump complete
--

\unrestrict rtc6O5GAHbimrFm5neiA4PmsW9Pc4kgr2bm0Fu22Eu6ARKmoydTTRae4BAhRg3l

--
-- PostgreSQL database dump
--

\restrict 9u6xk3X64ahq0FVeoOYWdjwnoePZwR4rQcuQ9dRQibnoT0IpxEmV8layoq0wsKz

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: customers; Type: TABLE; Schema: public; Owner: webstore
--

CREATE TABLE public.customers (
    id integer NOT NULL,
    phone character varying(20) NOT NULL,
    password_hash character varying(200) NOT NULL,
    name character varying(100) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    is_admin integer DEFAULT 0
);


ALTER TABLE public.customers OWNER TO webstore;

--
-- Name: customers_id_seq; Type: SEQUENCE; Schema: public; Owner: webstore
--

CREATE SEQUENCE public.customers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customers_id_seq OWNER TO webstore;

--
-- Name: customers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: webstore
--

ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;


--
-- Name: feedbacks; Type: TABLE; Schema: public; Owner: webstore
--

CREATE TABLE public.feedbacks (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    vin character varying(50),
    message text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(20) DEFAULT 'новый'::character varying
);


ALTER TABLE public.feedbacks OWNER TO webstore;

--
-- Name: feedbacks_id_seq; Type: SEQUENCE; Schema: public; Owner: webstore
--

CREATE SEQUENCE public.feedbacks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feedbacks_id_seq OWNER TO webstore;

--
-- Name: feedbacks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: webstore
--

ALTER SEQUENCE public.feedbacks_id_seq OWNED BY public.feedbacks.id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: webstore
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    order_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    price numeric(10,2) NOT NULL
);


ALTER TABLE public.order_items OWNER TO webstore;

--
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: webstore
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_items_id_seq OWNER TO webstore;

--
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: webstore
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: webstore
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    customer_id integer NOT NULL,
    order_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(50) DEFAULT 'новый'::character varying,
    total_amount numeric(10,2) DEFAULT 0
);


ALTER TABLE public.orders OWNER TO webstore;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: webstore
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO webstore;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: webstore
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: webstore
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    price numeric(10,2) NOT NULL,
    image_url character varying(200) DEFAULT 'images/default.jpg'::character varying,
    stock integer DEFAULT 0
);


ALTER TABLE public.products OWNER TO webstore;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: webstore
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO webstore;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: webstore
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);


--
-- Name: feedbacks id; Type: DEFAULT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.feedbacks ALTER COLUMN id SET DEFAULT nextval('public.feedbacks_id_seq'::regclass);


--
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: webstore
--

COPY public.customers (id, phone, password_hash, name, created_at, is_admin) FROM stdin;
2	+375295742878	scrypt:32768:8:1$fSNU6MnZPj4Sr6p2$616ce51a0099edcd275fb8a0a6dde214647a40dccee8b1369b9b171c86eb6e2ccf0d7067b243d4d04e6081dc7e446c0970bb3341e0a5a9e5e8a27fa450a550e0	Юрий	2026-06-06 10:18:31.107299	0
1	+1234567890	scrypt:32768:8:1$nhA88Hyd8wqUc88n$f08ec02b5fa706b1ef45b1e9a76f94aafe1bd6e49e61f8d4c064307cf82f7057957927eaecd5fde1fdb1e88c1e65873d0812f361a339dc29a06d9ab264ecefcc	Admin	2026-06-06 10:13:35.269953	1
\.


--
-- Data for Name: feedbacks; Type: TABLE DATA; Schema: public; Owner: webstore
--

COPY public.feedbacks (id, name, vin, message, created_at, status) FROM stdin;
1	Юрий	ZZZ615165151	Шины 205*55*R16	2026-06-06 11:20:54.718198	новый
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: webstore
--

COPY public.order_items (id, order_id, product_id, quantity, price) FROM stdin;
1	1	1	1	8000.00
2	2	1	2	8000.00
3	2	2	1	5000.00
4	2	3	1	15000.00
5	2	4	1	1000.00
6	3	1	1	8000.00
7	3	2	1	5000.00
8	3	3	1	15000.00
9	3	4	1	1000.00
16	6	1	1	8000.00
17	6	2	1	5000.00
18	6	3	1	15000.00
19	6	4	1	1000.00
20	7	1	1	8000.00
21	7	2	1	5000.00
22	7	3	1	15000.00
23	7	4	1	1000.00
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: webstore
--

COPY public.orders (id, customer_id, order_date, status, total_amount) FROM stdin;
1	2	2026-06-06 10:19:00.740969	новый	8000.00
2	2	2026-06-06 12:19:57.215503	новый	37000.00
3	2	2026-06-06 12:25:01.326237	новый	29000.00
6	1	2026-06-06 15:49:32.391387	новый	29000.00
7	2	2026-06-06 16:36:54.941487	новый	29000.00
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: webstore
--

COPY public.products (id, name, description, price, image_url, stock) FROM stdin;
1	Масло моторное	Синтетическое\r\n5w-40\r\nShell\r\n4л	8000.00	images/product_1.jpg	4
2	Тормозные колодки	Brembo\r\n300мм	5000.00	images/product_2.jpg	2
3	Аккумулятор	Zubr\r\n65A/h\r\n12v	15000.00	images/product_3.jpg	16
4	Фильтры	Масляный\r\nвставка	1000.00	images/product_4.jpg	96
\.


--
-- Name: customers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: webstore
--

SELECT pg_catalog.setval('public.customers_id_seq', 2, true);


--
-- Name: feedbacks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: webstore
--

SELECT pg_catalog.setval('public.feedbacks_id_seq', 1, true);


--
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: webstore
--

SELECT pg_catalog.setval('public.order_items_id_seq', 23, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: webstore
--

SELECT pg_catalog.setval('public.orders_id_seq', 7, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: webstore
--

SELECT pg_catalog.setval('public.products_id_seq', 4, true);


--
-- Name: customers customers_phone_key; Type: CONSTRAINT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_phone_key UNIQUE (phone);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: feedbacks feedbacks_pkey; Type: CONSTRAINT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.feedbacks
    ADD CONSTRAINT feedbacks_pkey PRIMARY KEY (id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- Name: order_items order_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: orders orders_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: webstore
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 9u6xk3X64ahq0FVeoOYWdjwnoePZwR4rQcuQ9dRQibnoT0IpxEmV8layoq0wsKz

