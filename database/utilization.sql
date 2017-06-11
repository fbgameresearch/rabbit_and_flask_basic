--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: cpu; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE cpu (
    host_id integer NOT NULL,
    name character varying NOT NULL,
    "time" character varying NOT NULL,
    read character varying,
    usage_cpu character varying
);


ALTER TABLE cpu OWNER TO postgres;

--
-- Name: net; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE net (
    host_id integer NOT NULL,
    name character varying NOT NULL,
    "time" character varying NOT NULL,
    read character varying,
    rx_bytes character varying,
    tx_bytes character varying
);


ALTER TABLE net OWNER TO postgres;

--
-- Name: ram; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE ram (
    host_id integer NOT NULL,
    name character varying NOT NULL,
    "time" character varying NOT NULL,
    read character varying,
    usage_ram character varying,
    limit_ram character varying
);


ALTER TABLE ram OWNER TO postgres;

--
-- Data for Name: cpu; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY cpu (host_id, name, "time", read, usage_cpu) FROM stdin;
\.


--
-- Data for Name: net; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY net (host_id, name, "time", read, rx_bytes, tx_bytes) FROM stdin;
\.


--
-- Data for Name: ram; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY ram (host_id, name, "time", read, usage_ram, limit_ram) FROM stdin;
\.


--
-- Name: cpu cpu_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY cpu
    ADD CONSTRAINT cpu_pkey PRIMARY KEY (host_id, name, "time");


--
-- Name: net net_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY net
    ADD CONSTRAINT net_pkey PRIMARY KEY (host_id, name, "time");


--
-- Name: ram ram_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ram
    ADD CONSTRAINT ram_pkey PRIMARY KEY (host_id, name, "time");


--
-- PostgreSQL database dump complete
--
