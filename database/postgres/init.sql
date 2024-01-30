--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

-- Started on 2024-01-28 22:40:49

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 16384)
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- TOC entry 4818 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 221 (class 1259 OID 16441)
-- Name: admin_attendance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin_attendance (
    attendance_id integer NOT NULL,
    admin_id integer NOT NULL,
    attendance_date date NOT NULL
);


ALTER TABLE public.admin_attendance OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16411)
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    admin_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(128) NOT NULL,
    full_name character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    department_id integer
);


ALTER TABLE public.admins OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16406)
-- Name: departments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departments (
    department_id integer NOT NULL,
    department_name character varying(50) NOT NULL
);


ALTER TABLE public.departments OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16432)
-- Name: user_attendance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_attendance (
    attendance_id integer NOT NULL,
    user_id integer,
    attendance_date date
);


ALTER TABLE public.user_attendance OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16431)
-- Name: user_attendance_attendance_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_attendance_attendance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_attendance_attendance_id_seq OWNER TO postgres;

--
-- TOC entry 4819 (class 0 OID 0)
-- Dependencies: 219
-- Name: user_attendance_attendance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_attendance_attendance_id_seq OWNED BY public.user_attendance.attendance_id;


--
-- TOC entry 218 (class 1259 OID 16421)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(128) NOT NULL,
    full_name character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    department_id integer NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 4651 (class 2604 OID 16435)
-- Name: user_attendance attendance_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_attendance ALTER COLUMN attendance_id SET DEFAULT nextval('public.user_attendance_attendance_id_seq'::regclass);


--
-- TOC entry 4812 (class 0 OID 16441)
-- Dependencies: 221
-- Data for Name: admin_attendance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admin_attendance (attendance_id, admin_id, attendance_date) FROM stdin;
\.


--
-- TOC entry 4808 (class 0 OID 16411)
-- Dependencies: 217
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admins (admin_id, username, password, full_name, email, department_id) FROM stdin;
\.


--
-- TOC entry 4807 (class 0 OID 16406)
-- Dependencies: 216
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.departments (department_id, department_name) FROM stdin;
\.


--
-- TOC entry 4811 (class 0 OID 16432)
-- Dependencies: 220
-- Data for Name: user_attendance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_attendance (attendance_id, user_id, attendance_date) FROM stdin;
\.


--
-- TOC entry 4809 (class 0 OID 16421)
-- Dependencies: 218
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, username, password, full_name, email, department_id) FROM stdin;
\.


--
-- TOC entry 4820 (class 0 OID 0)
-- Dependencies: 219
-- Name: user_attendance_attendance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_attendance_attendance_id_seq', 1, false);


--
-- TOC entry 4659 (class 2606 OID 16445)
-- Name: admin_attendance admin_attendance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_attendance
    ADD CONSTRAINT admin_attendance_pkey PRIMARY KEY (attendance_id);


--
-- TOC entry 4655 (class 2606 OID 16415)
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (admin_id);


--
-- TOC entry 4653 (class 2606 OID 16410)
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (department_id);


--
-- TOC entry 4657 (class 2606 OID 16425)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4663 (class 2606 OID 16446)
-- Name: admin_attendance admin_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_attendance
    ADD CONSTRAINT admin_id FOREIGN KEY (admin_id) REFERENCES public.admins(admin_id);


--
-- TOC entry 4660 (class 2606 OID 16416)
-- Name: admins department_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT department_id FOREIGN KEY (department_id) REFERENCES public.departments(department_id);


--
-- TOC entry 4661 (class 2606 OID 16426)
-- Name: users department_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT department_id FOREIGN KEY (department_id) REFERENCES public.departments(department_id);


--
-- TOC entry 4662 (class 2606 OID 16436)
-- Name: user_attendance user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_attendance
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id);


-- Completed on 2024-01-28 22:40:49

--
-- PostgreSQL database dump complete
--

