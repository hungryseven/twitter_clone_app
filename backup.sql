--
-- PostgreSQL database dump
--

-- Dumped from database version 14.3
-- Dumped by pg_dump version 14.3

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
-- Name: citext; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;


--
-- Name: EXTENSION citext; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION citext IS 'data type for case-insensitive character strings';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: authorization_customuser; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authorization_customuser (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username public.citext NOT NULL,
    email public.citext NOT NULL,
    profile_name character varying(50) NOT NULL,
    about character varying(160) NOT NULL,
    location character varying(30) NOT NULL,
    website character varying(100) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    profile_photo character varying(100) NOT NULL
);


--
-- Name: authorization_customuser_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authorization_customuser_groups (
    id bigint NOT NULL,
    customuser_id bigint NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: authorization_customuser_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.authorization_customuser_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: authorization_customuser_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.authorization_customuser_groups_id_seq OWNED BY public.authorization_customuser_groups.id;


--
-- Name: authorization_customuser_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.authorization_customuser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: authorization_customuser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.authorization_customuser_id_seq OWNED BY public.authorization_customuser.id;


--
-- Name: authorization_customuser_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authorization_customuser_user_permissions (
    id bigint NOT NULL,
    customuser_id bigint NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: authorization_customuser_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.authorization_customuser_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: authorization_customuser_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.authorization_customuser_user_permissions_id_seq OWNED BY public.authorization_customuser_user_permissions.id;


--
-- Name: authorization_footerlinks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authorization_footerlinks (
    id bigint NOT NULL,
    title public.citext NOT NULL,
    url character varying(200) NOT NULL
);


--
-- Name: authorization_footerlinks_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.authorization_footerlinks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: authorization_footerlinks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.authorization_footerlinks_id_seq OWNED BY public.authorization_footerlinks.id;


--
-- Name: authorization_userfollow; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authorization_userfollow (
    id bigint NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    followee_id bigint NOT NULL,
    follower_id bigint NOT NULL
);


--
-- Name: authorization_userfollow_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.authorization_userfollow_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: authorization_userfollow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.authorization_userfollow_id_seq OWNED BY public.authorization_userfollow.id;


--
-- Name: authorization_usernotification; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authorization_usernotification (
    id bigint NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    is_viewed boolean NOT NULL,
    tweet_id bigint NOT NULL,
    user_id bigint NOT NULL
);


--
-- Name: authorization_usernotification_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.authorization_usernotification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: authorization_usernotification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.authorization_usernotification_id_seq OWNED BY public.authorization_usernotification.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: tweets_tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tweets_tag (
    id bigint NOT NULL,
    tag_name public.citext NOT NULL
);


--
-- Name: tweets_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tweets_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tweets_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tweets_tag_id_seq OWNED BY public.tweets_tag.id;


--
-- Name: tweets_tag_related_tweets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tweets_tag_related_tweets (
    id bigint NOT NULL,
    tag_id bigint NOT NULL,
    tweet_id bigint NOT NULL
);


--
-- Name: tweets_tag_related_tweets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tweets_tag_related_tweets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tweets_tag_related_tweets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tweets_tag_related_tweets_id_seq OWNED BY public.tweets_tag_related_tweets.id;


--
-- Name: tweets_tweet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tweets_tweet (
    id bigint NOT NULL,
    text character varying(140) NOT NULL,
    pub_date timestamp with time zone NOT NULL,
    lft integer NOT NULL,
    rght integer NOT NULL,
    tree_id integer NOT NULL,
    level integer NOT NULL,
    parent_id bigint,
    user_id bigint NOT NULL,
    CONSTRAINT tweets_tweet_level_check CHECK ((level >= 0)),
    CONSTRAINT tweets_tweet_lft_check CHECK ((lft >= 0)),
    CONSTRAINT tweets_tweet_rght_check CHECK ((rght >= 0)),
    CONSTRAINT tweets_tweet_tree_id_check CHECK ((tree_id >= 0))
);


--
-- Name: tweets_tweet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tweets_tweet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tweets_tweet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tweets_tweet_id_seq OWNED BY public.tweets_tweet.id;


--
-- Name: tweets_tweetbookmark; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tweets_tweetbookmark (
    id bigint NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    tweet_id bigint NOT NULL,
    user_id bigint NOT NULL
);


--
-- Name: tweets_tweetbookmark_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tweets_tweetbookmark_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tweets_tweetbookmark_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tweets_tweetbookmark_id_seq OWNED BY public.tweets_tweetbookmark.id;


--
-- Name: tweets_tweetlike; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tweets_tweetlike (
    id bigint NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    tweet_id bigint NOT NULL,
    user_id bigint NOT NULL
);


--
-- Name: tweets_tweetlike_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tweets_tweetlike_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tweets_tweetlike_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tweets_tweetlike_id_seq OWNED BY public.tweets_tweetlike.id;


--
-- Name: tweets_tweetretweet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tweets_tweetretweet (
    id bigint NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    tweet_id bigint NOT NULL,
    user_id bigint NOT NULL
);


--
-- Name: tweets_tweetretweet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tweets_tweetretweet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tweets_tweetretweet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tweets_tweetretweet_id_seq OWNED BY public.tweets_tweetretweet.id;


--
-- Name: tweets_tweetusers_parents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tweets_tweetusers_parents (
    id bigint NOT NULL,
    level smallint NOT NULL,
    tweet_id bigint NOT NULL,
    user_id bigint NOT NULL,
    CONSTRAINT tweets_tweetusers_parents_level_check CHECK ((level >= 0))
);


--
-- Name: tweets_tweetusers_parents_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tweets_tweetusers_parents_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tweets_tweetusers_parents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tweets_tweetusers_parents_id_seq OWNED BY public.tweets_tweetusers_parents.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: authorization_customuser id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser ALTER COLUMN id SET DEFAULT nextval('public.authorization_customuser_id_seq'::regclass);


--
-- Name: authorization_customuser_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser_groups ALTER COLUMN id SET DEFAULT nextval('public.authorization_customuser_groups_id_seq'::regclass);


--
-- Name: authorization_customuser_user_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.authorization_customuser_user_permissions_id_seq'::regclass);


--
-- Name: authorization_footerlinks id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_footerlinks ALTER COLUMN id SET DEFAULT nextval('public.authorization_footerlinks_id_seq'::regclass);


--
-- Name: authorization_userfollow id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_userfollow ALTER COLUMN id SET DEFAULT nextval('public.authorization_userfollow_id_seq'::regclass);


--
-- Name: authorization_usernotification id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_usernotification ALTER COLUMN id SET DEFAULT nextval('public.authorization_usernotification_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: tweets_tag id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tag ALTER COLUMN id SET DEFAULT nextval('public.tweets_tag_id_seq'::regclass);


--
-- Name: tweets_tag_related_tweets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tag_related_tweets ALTER COLUMN id SET DEFAULT nextval('public.tweets_tag_related_tweets_id_seq'::regclass);


--
-- Name: tweets_tweet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweet ALTER COLUMN id SET DEFAULT nextval('public.tweets_tweet_id_seq'::regclass);


--
-- Name: tweets_tweetbookmark id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetbookmark ALTER COLUMN id SET DEFAULT nextval('public.tweets_tweetbookmark_id_seq'::regclass);


--
-- Name: tweets_tweetlike id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetlike ALTER COLUMN id SET DEFAULT nextval('public.tweets_tweetlike_id_seq'::regclass);


--
-- Name: tweets_tweetretweet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetretweet ALTER COLUMN id SET DEFAULT nextval('public.tweets_tweetretweet_id_seq'::regclass);


--
-- Name: tweets_tweetusers_parents id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetusers_parents ALTER COLUMN id SET DEFAULT nextval('public.tweets_tweetusers_parents_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add ссылку футера	1	add_footerlinks
2	Can change ссылку футера	1	change_footerlinks
3	Can delete ссылку футера	1	delete_footerlinks
4	Can view ссылку футера	1	view_footerlinks
5	Can add пользователя	2	add_customuser
6	Can change пользователя	2	change_customuser
7	Can delete пользователя	2	delete_customuser
8	Can view пользователя	2	view_customuser
9	Can add user follow	3	add_userfollow
10	Can change user follow	3	change_userfollow
11	Can delete user follow	3	delete_userfollow
12	Can view user follow	3	view_userfollow
13	Can add user notification	4	add_usernotification
14	Can change user notification	4	change_usernotification
15	Can delete user notification	4	delete_usernotification
16	Can view user notification	4	view_usernotification
17	Can add твит	5	add_tweet
18	Can change твит	5	change_tweet
19	Can delete твит	5	delete_tweet
20	Can view твит	5	view_tweet
21	Can add tweet retweet	6	add_tweetretweet
22	Can change tweet retweet	6	change_tweetretweet
23	Can delete tweet retweet	6	delete_tweetretweet
24	Can view tweet retweet	6	view_tweetretweet
25	Can add tweet like	7	add_tweetlike
26	Can change tweet like	7	change_tweetlike
27	Can delete tweet like	7	delete_tweetlike
28	Can view tweet like	7	view_tweetlike
29	Can add tweet bookmark	8	add_tweetbookmark
30	Can change tweet bookmark	8	change_tweetbookmark
31	Can delete tweet bookmark	8	delete_tweetbookmark
32	Can view tweet bookmark	8	view_tweetbookmark
33	Can add тег	9	add_tag
34	Can change тег	9	change_tag
35	Can delete тег	9	delete_tag
36	Can view тег	9	view_tag
37	Can add tweet users_ parents	10	add_tweetusers_parents
38	Can change tweet users_ parents	10	change_tweetusers_parents
39	Can delete tweet users_ parents	10	delete_tweetusers_parents
40	Can view tweet users_ parents	10	view_tweetusers_parents
41	Can add log entry	11	add_logentry
42	Can change log entry	11	change_logentry
43	Can delete log entry	11	delete_logentry
44	Can view log entry	11	view_logentry
45	Can add permission	12	add_permission
46	Can change permission	12	change_permission
47	Can delete permission	12	delete_permission
48	Can view permission	12	view_permission
49	Can add group	13	add_group
50	Can change group	13	change_group
51	Can delete group	13	delete_group
52	Can view group	13	view_group
53	Can add content type	14	add_contenttype
54	Can change content type	14	change_contenttype
55	Can delete content type	14	delete_contenttype
56	Can view content type	14	view_contenttype
57	Can add session	15	add_session
58	Can change session	15	change_session
59	Can delete session	15	delete_session
60	Can view session	15	view_session
\.


--
-- Data for Name: authorization_customuser; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.authorization_customuser (id, password, last_login, is_superuser, username, email, profile_name, about, location, website, is_staff, is_active, date_joined, profile_photo) FROM stdin;
3	pbkdf2_sha256$320000$4VcPGPrHJB8rzY05ZM9VME$lo2tYBKTW65tbNKG+3smzJT4vu1WfonLEtcfCBnKw2E=	2022-05-31 19:38:20.781211+05	f	username	semerikovsahsa@yandex.ru	Юзернейм	Просто юзернейм	Абсолютно неважно		f	t	2022-05-31 19:38:14.973897+05	photos/username/2b480486a917b5e25c8b37d6df7d305e.jpg
4	pbkdf2_sha256$320000$7gPJ7boMPjO2llYZqaHPMK$68UsAyYLte9d7ZUzsZqW8tpxyUfWeQwW3oimPAlEamQ=	2022-05-31 21:19:04.831256+05	f	elonmusk	elonmusk@gmail.com	Elon Musk				f	t	2022-05-31 21:18:51.817539+05	photos/elonmusk/Nyn1HZWF_400x400.jpg
1	pbkdf2_sha256$320000$F4kkMEa2j201L4szy5NWrR$cy3yOc9yqe/BNGysu9+fSEesBrBymKQANOwpTSi9ksU=	2022-05-31 21:27:31.988517+05	t	administrator	jgutik74@gmail.com	Admin		Челябинск	http://t.me/semerikov_alexandr	t	t	2022-05-31 18:37:16.300625+05	photos/administrator/3f61e0c6c26a7efa236ded6679bm-aksessuary-detskaya-shapochka-dlya-mal_i2FItI9.jpg
5	pbkdf2_sha256$320000$iwVvCydauW4YRrC7dnKJCR$Aa660sY0i9tjg/vQYeRpHOKs9KS15ZXS7v1CAmNBUvY=	2022-05-31 21:29:16.173246+05	f	LiverpoolFC	LFC@gmail.com	Liverpool FC	Official Twitter account of Liverpool Football Club 🔴\r\nStop The Hate, Report It. ✊	Anfield	https://linktr.ee/liverpoolfootballclub	f	t	2022-05-31 21:29:00.298352+05	photos/LiverpoolFC/waX3gy16_400x400.jpg
2	pbkdf2_sha256$320000$p48q7Hq67ncSdRF4nyLp1o$fWvKJ4jVcIDwkrgzvp+yCH/AmL42fyLEYy4yQegLx44=	2022-05-31 22:07:17.862978+05	f	alexandr_sem	alexandrsem7@gmail.com	Александр	Местный клоун.\r\nНаписал это детище для портфолио.	Челябинск	https://vk.com/id165558882	f	t	2022-05-31 19:21:35.322248+05	photos/alexandr_sem/dt7EXWK7z6o9qYloEtVu8S1Jr-bR3C-7LLsqVGkO7hbigJhTS6yui7-z54vnMU2UswMR_F9qjBzN.jpg
\.


--
-- Data for Name: authorization_customuser_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.authorization_customuser_groups (id, customuser_id, group_id) FROM stdin;
\.


--
-- Data for Name: authorization_customuser_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.authorization_customuser_user_permissions (id, customuser_id, permission_id) FROM stdin;
\.


--
-- Data for Name: authorization_footerlinks; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.authorization_footerlinks (id, title, url) FROM stdin;
\.


--
-- Data for Name: authorization_userfollow; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.authorization_userfollow (id, "timestamp", followee_id, follower_id) FROM stdin;
1	2022-05-31 19:21:57.77684+05	1	2
2	2022-05-31 19:38:30.658178+05	1	3
3	2022-05-31 19:38:35.060456+05	2	3
4	2022-05-31 21:27:15.054734+05	1	4
5	2022-05-31 21:27:18.575386+05	2	4
6	2022-05-31 21:27:40.608267+05	2	1
7	2022-05-31 21:27:41.332805+05	4	1
8	2022-05-31 22:08:42.355102+05	5	2
\.


--
-- Data for Name: authorization_usernotification; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.authorization_usernotification (id, "timestamp", is_viewed, tweet_id, user_id) FROM stdin;
1	2022-05-31 19:25:39.78142+05	t	2	1
3	2022-05-31 21:08:01.548335+05	t	15	1
2	2022-05-31 21:08:01.548335+05	t	15	2
4	2022-05-31 22:08:09.258288+05	f	55	3
5	2022-05-31 22:08:33.689428+05	f	56	1
6	2022-05-31 22:08:33.689428+05	f	56	3
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2022-05-31 19:21:35.340217+05	2	alexandr_sem	1	[{"added": {}}]	2	1
2	2022-05-31 19:29:11.082641+05	4	Раз вы каким-то образом сюда забрели (скорее всего ...	3		5	1
3	2022-05-31 19:38:14.981979+05	3	username	1	[{"added": {}}]	2	1
4	2022-05-31 21:18:51.831864+05	4	elonmusk	1	[{"added": {}}]	2	1
5	2022-05-31 21:29:00.304992+05	5	LiverpoolFC	1	[{"added": {}}]	2	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	authorization	footerlinks
2	authorization	customuser
3	authorization	userfollow
4	authorization	usernotification
5	tweets	tweet
6	tweets	tweetretweet
7	tweets	tweetlike
8	tweets	tweetbookmark
9	tweets	tag
10	tweets	tweetusers_parents
11	admin	logentry
12	auth	permission
13	auth	group
14	contenttypes	contenttype
15	sessions	session
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2022-05-31 17:51:21.802208+05
2	contenttypes	0002_remove_content_type_name	2022-05-31 17:51:21.849822+05
3	auth	0001_initial	2022-05-31 17:51:22.456524+05
4	auth	0002_alter_permission_name_max_length	2022-05-31 17:51:22.48526+05
5	auth	0003_alter_user_email_max_length	2022-05-31 17:51:22.504892+05
6	auth	0004_alter_user_username_opts	2022-05-31 17:51:22.527043+05
7	auth	0005_alter_user_last_login_null	2022-05-31 17:51:22.549255+05
8	auth	0006_require_contenttypes_0002	2022-05-31 17:51:22.56623+05
9	auth	0007_alter_validators_add_error_messages	2022-05-31 17:51:22.596335+05
10	auth	0008_alter_user_username_max_length	2022-05-31 17:51:22.617127+05
11	auth	0009_alter_user_last_name_max_length	2022-05-31 17:51:22.640398+05
12	auth	0010_alter_group_name_max_length	2022-05-31 17:51:22.662349+05
13	auth	0011_update_proxy_permissions	2022-05-31 17:51:22.683466+05
14	auth	0012_alter_user_first_name_max_length	2022-05-31 17:51:22.704596+05
15	authorization	0001_initial	2022-05-31 17:51:25.871807+05
16	admin	0001_initial	2022-05-31 17:51:26.190035+05
17	admin	0002_logentry_remove_auto_add	2022-05-31 17:51:26.22444+05
18	admin	0003_logentry_add_action_flag_choices	2022-05-31 17:51:26.255445+05
19	authorization	0002_tweet_model	2022-05-31 17:51:26.346622+05
20	tweets	0001_tweet_model	2022-05-31 17:51:28.308163+05
21	tweets	0002_notifications	2022-05-31 17:51:28.343741+05
22	authorization	0003_photo_field	2022-05-31 17:51:28.388201+05
23	authorization	0004_follow_fields	2022-05-31 17:51:28.730608+05
24	authorization	0005_notifications	2022-05-31 17:51:29.072406+05
25	authorization	0006_users_parents_field	2022-05-31 17:51:29.102947+05
26	sessions	0001_initial	2022-05-31 17:51:30.449217+05
27	tweets	0003_tags_models	2022-05-31 17:51:31.076385+05
28	tweets	0004_users_parents_field	2022-05-31 17:51:31.505726+05
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
hc1uznti45wy1n0xvcevjawviiliaa4l	.eJxVi0sOwiAQQO_C2jTQCgMu7UGagRkCMZakwEbj3bWmC92-z1Ms2FtaeuVtySQuYhSnX-Yx3Hjdxc7Klh_YclmHb3HIYe61lfv1SP_-hDV9ZklB8wioJqDgjTPRWQIEkpNyPnCMJLXXBBxsMBaiAsIzRekls3dGvN4T7Tl7:1nw5Kw:BRX6VHU4z2_MhBEkJQx9RBjwJaM05xc0fhfk5zkpnMs	2022-06-14 22:07:18.202704+05
\.


--
-- Data for Name: tweets_tag; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tweets_tag (id, tag_name) FROM stdin;
1	#hello
2	#poor
3	#twitter
4	#clone
5	#first
6	#tweet
7	#finally
8	#gj
9	#vsem
10	#o4en
11	#insteresna
12	#eta
13	#situatsia
14	#UCLfinal
15	#We
16	#will
17	#never
18	#walk
19	#alone
\.


--
-- Data for Name: tweets_tag_related_tweets; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tweets_tag_related_tweets (id, tag_id, tweet_id) FROM stdin;
1	1	1
2	2	1
3	3	1
4	4	1
5	5	1
6	6	1
13	7	2
15	8	13
17	6	15
19	9	16
20	10	16
21	11	16
22	12	16
23	13	16
29	8	18
31	14	32
33	14	33
35	14	34
37	14	35
39	14	36
41	14	37
43	14	38
45	14	39
47	14	40
49	14	41
51	14	42
53	14	43
55	14	44
57	14	45
59	14	46
61	14	47
63	14	48
65	14	49
67	14	50
69	14	51
71	14	52
73	14	53
75	14	54
77	15	57
78	16	57
79	17	57
80	18	57
81	19	57
\.


--
-- Data for Name: tweets_tweet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tweets_tweet (id, text, pub_date, lft, rght, tree_id, level, parent_id, user_id) FROM stdin;
23	Great potential to lift people out of poverty. Providing Internet is teaching people to fish	2022-05-31 21:21:48.379772+05	2	3	10	1	22	4
3	Еще скоро эта штука будет доступна на хероку\r\nНадеюсь получится импортировать туда локальную бд	2022-05-31 19:26:39.241992+05	1	2	3	0	\N	2
12	Сейчас как залью на хероку по фасту накинусь на DRF и docker, потому что время поджимает	2022-05-31 19:37:03.043661+05	1	2	6	0	\N	2
24	Tesla merch can be bought with Doge, soon SpaceX merch too	2022-05-31 21:22:03.225319+05	1	2	11	0	\N	4
6	2/3\r\nЭта штука для заказа еды японской кухни с возможностью регистрации по номеру телефона, выбора различных блюд и добавления их в корзину	2022-05-31 19:31:17.69692+05	2	3	4	1	5	2
7	3/3 \r\nРабочая функция оформления заказа с возможностью выбора дня и времени доставки\r\nРабочий профиль с данными, адресами, историей заказов	2022-05-31 19:33:17.514928+05	4	5	4	1	5	2
31	I’m a fan of Jack btw. Wish he would stay on the board, but I understand that he needs to move on.	2022-05-31 21:24:23.387246+05	3	4	14	2	30	4
25	Ya know, it’s pretty damn great to be able to talk to people from all walks of life and many countries on Twitter!	2022-05-31 21:22:34.649534+05	1	4	12	0	\N	4
9	Обучался полностью сам, не заглядывая на платные курсы\r\nИз курсов максимум прошел базовый питон и sql-тренажер на степике	2022-05-31 19:35:09.59887+05	2	5	5	1	8	2
10	Кстати советую их для новичков, очень полезно будет	2022-05-31 19:35:24.608055+05	3	4	5	2	9	2
8	На самом деле старался сделать что-то не особо тривиальное для портфолио	2022-05-31 19:34:20.849366+05	1	8	5	0	\N	2
11	Ну и еще какие-то курсы по мелочи вроде линукса, html и css (хотя на степике и в интернете они такое себе)	2022-05-31 19:36:28.788427+05	6	7	5	1	8	2
15	Твит ради твита\r\n@alexandr_sem @administrator\r\n#tweet	2022-05-31 21:08:01.548335+05	1	2	7	0	\N	3
1	Мой первый твит здесь \r\n#hello #poor #twitter #clone #first #tweet	2022-05-31 18:53:36.341434+05	1	4	1	0	\N	1
16	Всем очень интересно конечно\r\n#vsem #o4en #insteresna #eta #situatsia	2022-05-31 21:13:37.975954+05	2	3	1	1	1	3
5	1/3\r\nРаз вы каким-то образом сюда забрели (скорее всего обманом), то гляньте первый проект на фласке\r\ndelivery-web-app.herokuapp.com	2022-05-31 19:30:23.087964+05	1	12	4	0	\N	2
13	Чел хорош #gj	2022-05-31 19:39:04.878894+05	6	11	4	1	5	3
26	So much to be learned, even from the harshest critics. \r\nBasically … I’m just saying I love all you crazy peopl	2022-05-31 21:22:51.825414+05	2	3	12	1	25	4
19	Tomorrow will be the first sunrise of the rest of ur life – make it what u want	2022-05-31 21:20:42.875047+05	1	4	8	0	\N	4
20	And remember that happiness is a choice	2022-05-31 21:20:55.592673+05	2	3	8	1	19	4
21	When thinking about deep time, what is more astounding is to think about how much time is ahead!	2022-05-31 21:21:21.225331+05	1	2	9	0	\N	4
22	One Starlink can provide Internet for an entire school of hundreds of students	2022-05-31 21:21:37.080982+05	1	4	10	0	\N	4
27	Use of the word “billionaire” as a pejorative is morally wrong & dumb 😛	2022-05-31 21:23:28.741906+05	1	4	13	0	\N	4
28	If the reason for it is building products that make millions of people happy	2022-05-31 21:23:41.068287+05	2	3	13	1	27	4
32	1’ – We are underway in Paris…ALLEZ LES ROUGES! 🔴\r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 21:31:22.939915+05	1	2	15	0	\N	5
33	10' - Salah picks out Mane, who looks to cut the ball back from the byline for Diaz.\r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 21:58:42.514956+05	1	2	16	0	\N	5
29	Jack off the board!	2022-05-31 21:24:02.965209+05	1	6	14	0	\N	4
30	(Of Twitter)	2022-05-31 21:24:11.609257+05	2	5	14	1	29	4
34	15' - Vinicius looks to create something down the left, but Konate steps across and win the ball back.\r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 21:59:52.133527+05	1	2	17	0	\N	5
35	16' - Courtois is forced into a smart first save, as Trent's low ball is flicked goalwards by Salah.\r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 22:00:02.75215+05	1	2	18	0	\N	5
36	19' - Mane and Salah work the ball into the feet of Trent on the corner of the box, but his shot goes over.\r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 22:00:34.727963+05	1	2	19	0	\N	5
37	21' - So close! Mane's sharp movement sees him get away from Casemiro and Militao. Saved on to the post.\r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 22:00:43.30923+05	1	2	20	0	\N	5
38	25' - Vinicius sends in a cross that is swerving, Benzema waits for it but Alisson claims comfortably. \r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 22:00:55.784704+05	1	2	21	0	\N	5
39	35' - Konate does brilliantly to break the lines, he finds Trent out wide. Courtois saves.\r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 22:01:18.166701+05	1	2	22	0	\N	5
40	41' - Robertson delivers a corner, which is headed out as far as Henderson. His powerful strike drifts wide.\r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 22:01:26.192049+05	1	2	23	0	\N	5
41	43' - Benzema has the ball in the. He's ruled offside and now the VAR checking it.\r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 22:02:12.006581+05	1	2	24	0	\N	5
42	45+1' - After a short delay, the check is over and the original decision of offside stands.\r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 22:02:21.507871+05	1	2	25	0	\N	5
43	We go in level at the break.\r\n\r\n#UCLfinal	2022-05-31 22:02:29.879403+05	1	2	26	0	\N	5
14	Сча затестим шо тут как	2022-05-31 19:39:25.014798+05	2	7	2	1	2	3
44	46' - We're back underway in Paris. COME ON REDMEN!!!\r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 22:02:36.138336+05	1	2	27	0	\N	5
45	47' - Trent sends in an excellent cross towards Diaz. Carvajal does enough at the back post to clear.\r\n\r\n[0-0]\r\n\r\n#UCLfinal	2022-05-31 22:03:00.619816+05	1	2	28	0	\N	5
46	59' - Goal for Real Madrid. Vinicius. \r\n\r\n[0-1]\r\n\r\n#UCLfinal	2022-05-31 22:03:07.037156+05	1	2	29	0	\N	5
47	63' - Fabinho goes into the book for a late challenge.\r\n\r\n[0-1]\r\n\r\n#UCLfinal	2022-05-31 22:03:12.655931+05	1	2	30	0	\N	5
48	65' - Diaz is replaced by Jota in our first change.\r\n\r\n[0-1]\r\n\r\n#UCLfinal	2022-05-31 22:03:18.332549+05	1	2	31	0	\N	5
49	69' - Jota heads Henderson's deep ball in across goal, Salah reaches it but the angle is too tight.\r\n\r\n[0-1]\r\n\r\n#UCLfinal	2022-05-31 22:03:43.682547+05	1	2	32	0	\N	5
50	75' - Trent has a strike at goal, Jota tries to get the slightest of touches on the stretch to guide it on target.\r\n\r\n[0-1]\r\n\r\n#UCLfinal	2022-05-31 22:04:36.024961+05	1	2	33	0	\N	5
51	77' - Henderson is replaced by Keita. Thiago makes way for Firmino.\r\n\r\n[0-1]\r\n\r\n#UCLfinal	2022-05-31 22:04:41.962029+05	1	2	34	0	\N	5
52	80' - Salah's curling effort is touched on towards goal by the run of Jota. Courtois saves.\r\n\r\n[0-1]\r\n\r\n#UCLfinal	2022-05-31 22:06:00.011137+05	1	2	35	0	\N	5
53	83' - Salah's stunning first touch allows him to burst beyond Mendy. His effort forces another outstanding save. \r\n\r\n[0-1]\r\n\r\n#UCLfinal	2022-05-31 22:06:07.973779+05	1	2	36	0	\N	5
2	Хех, я написал какое-то подобие твиттера\r\n@administrator\r\n#finally	2022-05-31 19:25:39.78142+05	1	8	2	0	\N	2
17	И шо как?	2022-05-31 21:14:15.922627+05	3	6	2	2	14	1
55	Вроде сойдет? @username	2022-05-31 22:08:09.258288+05	4	5	2	3	17	2
18	Сыглы, чел реально хорош #gj	2022-05-31 21:14:51.152965+05	7	10	4	2	13	1
56	Благодарю благодарю @administrator @username	2022-05-31 22:08:33.689428+05	8	9	4	3	18	2
54	Defeat in the #UCLfinal	2022-05-31 22:06:56.408636+05	1	4	37	0	\N	5
57	Sad #We #will #never #walk #alone	2022-05-31 22:09:12.162258+05	2	3	37	1	54	2
\.


--
-- Data for Name: tweets_tweetbookmark; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tweets_tweetbookmark (id, "timestamp", tweet_id, user_id) FROM stdin;
\.


--
-- Data for Name: tweets_tweetlike; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tweets_tweetlike (id, "timestamp", tweet_id, user_id) FROM stdin;
1	2022-05-31 19:25:47.2153+05	1	2
4	2022-05-31 19:38:42.34795+05	5	3
5	2022-05-31 19:38:44.706231+05	6	3
6	2022-05-31 19:38:45.339091+05	7	3
10	2022-05-31 21:11:21.754115+05	1	3
11	2022-05-31 21:14:02.177434+05	5	1
14	2022-05-31 21:14:20.923626+05	2	1
15	2022-05-31 22:08:46.155502+05	54	2
\.


--
-- Data for Name: tweets_tweetretweet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tweets_tweetretweet (id, "timestamp", tweet_id, user_id) FROM stdin;
1	2022-05-31 19:25:48.527328+05	1	2
3	2022-05-31 19:38:48.210717+05	5	3
5	2022-05-31 20:06:32.548991+05	1	3
6	2022-05-31 22:08:44.486364+05	54	2
\.


--
-- Data for Name: tweets_tweetusers_parents; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tweets_tweetusers_parents (id, level, tweet_id, user_id) FROM stdin;
1	0	13	2
2	0	14	2
3	0	16	1
4	0	17	2
5	1	17	3
6	0	18	2
7	1	18	3
8	1	55	3
9	2	55	1
10	1	56	3
11	2	56	1
12	0	57	5
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 60, true);


--
-- Name: authorization_customuser_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.authorization_customuser_groups_id_seq', 1, false);


--
-- Name: authorization_customuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.authorization_customuser_id_seq', 5, true);


--
-- Name: authorization_customuser_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.authorization_customuser_user_permissions_id_seq', 1, false);


--
-- Name: authorization_footerlinks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.authorization_footerlinks_id_seq', 1, false);


--
-- Name: authorization_userfollow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.authorization_userfollow_id_seq', 8, true);


--
-- Name: authorization_usernotification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.authorization_usernotification_id_seq', 6, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 5, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 15, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 28, true);


--
-- Name: tweets_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tweets_tag_id_seq', 19, true);


--
-- Name: tweets_tag_related_tweets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tweets_tag_related_tweets_id_seq', 86, true);


--
-- Name: tweets_tweet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tweets_tweet_id_seq', 57, true);


--
-- Name: tweets_tweetbookmark_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tweets_tweetbookmark_id_seq', 1, false);


--
-- Name: tweets_tweetlike_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tweets_tweetlike_id_seq', 15, true);


--
-- Name: tweets_tweetretweet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tweets_tweetretweet_id_seq', 6, true);


--
-- Name: tweets_tweetusers_parents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tweets_tweetusers_parents_id_seq', 12, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: authorization_customuser_groups authorization_customuser_customuser_id_group_id_c2dc0310_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser_groups
    ADD CONSTRAINT authorization_customuser_customuser_id_group_id_c2dc0310_uniq UNIQUE (customuser_id, group_id);


--
-- Name: authorization_customuser_user_permissions authorization_customuser_customuser_id_permission_51b36e70_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser_user_permissions
    ADD CONSTRAINT authorization_customuser_customuser_id_permission_51b36e70_uniq UNIQUE (customuser_id, permission_id);


--
-- Name: authorization_customuser authorization_customuser_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser
    ADD CONSTRAINT authorization_customuser_email_key UNIQUE (email);


--
-- Name: authorization_customuser_groups authorization_customuser_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser_groups
    ADD CONSTRAINT authorization_customuser_groups_pkey PRIMARY KEY (id);


--
-- Name: authorization_customuser authorization_customuser_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser
    ADD CONSTRAINT authorization_customuser_pkey PRIMARY KEY (id);


--
-- Name: authorization_customuser_user_permissions authorization_customuser_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser_user_permissions
    ADD CONSTRAINT authorization_customuser_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: authorization_customuser authorization_customuser_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser
    ADD CONSTRAINT authorization_customuser_username_key UNIQUE (username);


--
-- Name: authorization_footerlinks authorization_footerlinks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_footerlinks
    ADD CONSTRAINT authorization_footerlinks_pkey PRIMARY KEY (id);


--
-- Name: authorization_footerlinks authorization_footerlinks_title_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_footerlinks
    ADD CONSTRAINT authorization_footerlinks_title_key UNIQUE (title);


--
-- Name: authorization_footerlinks authorization_footerlinks_url_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_footerlinks
    ADD CONSTRAINT authorization_footerlinks_url_key UNIQUE (url);


--
-- Name: authorization_userfollow authorization_userfollow_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_userfollow
    ADD CONSTRAINT authorization_userfollow_pkey PRIMARY KEY (id);


--
-- Name: authorization_usernotification authorization_usernotification_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_usernotification
    ADD CONSTRAINT authorization_usernotification_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: tweets_tag tweets_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tag
    ADD CONSTRAINT tweets_tag_pkey PRIMARY KEY (id);


--
-- Name: tweets_tag_related_tweets tweets_tag_related_tweets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tag_related_tweets
    ADD CONSTRAINT tweets_tag_related_tweets_pkey PRIMARY KEY (id);


--
-- Name: tweets_tag_related_tweets tweets_tag_related_tweets_tag_id_tweet_id_26ebaef3_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tag_related_tweets
    ADD CONSTRAINT tweets_tag_related_tweets_tag_id_tweet_id_26ebaef3_uniq UNIQUE (tag_id, tweet_id);


--
-- Name: tweets_tag tweets_tag_tag_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tag
    ADD CONSTRAINT tweets_tag_tag_name_key UNIQUE (tag_name);


--
-- Name: tweets_tweet tweets_tweet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweet
    ADD CONSTRAINT tweets_tweet_pkey PRIMARY KEY (id);


--
-- Name: tweets_tweetbookmark tweets_tweetbookmark_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetbookmark
    ADD CONSTRAINT tweets_tweetbookmark_pkey PRIMARY KEY (id);


--
-- Name: tweets_tweetlike tweets_tweetlike_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetlike
    ADD CONSTRAINT tweets_tweetlike_pkey PRIMARY KEY (id);


--
-- Name: tweets_tweetretweet tweets_tweetretweet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetretweet
    ADD CONSTRAINT tweets_tweetretweet_pkey PRIMARY KEY (id);


--
-- Name: tweets_tweetusers_parents tweets_tweetusers_parents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetusers_parents
    ADD CONSTRAINT tweets_tweetusers_parents_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: authorization_customuser_groups_customuser_id_da62a643; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authorization_customuser_groups_customuser_id_da62a643 ON public.authorization_customuser_groups USING btree (customuser_id);


--
-- Name: authorization_customuser_groups_group_id_0b5b1325; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authorization_customuser_groups_group_id_0b5b1325 ON public.authorization_customuser_groups USING btree (group_id);


--
-- Name: authorization_customuser_u_customuser_id_4937d13e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authorization_customuser_u_customuser_id_4937d13e ON public.authorization_customuser_user_permissions USING btree (customuser_id);


--
-- Name: authorization_customuser_u_permission_id_2f0f60f9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authorization_customuser_u_permission_id_2f0f60f9 ON public.authorization_customuser_user_permissions USING btree (permission_id);


--
-- Name: authorization_footerlinks_url_371f182f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authorization_footerlinks_url_371f182f_like ON public.authorization_footerlinks USING btree (url varchar_pattern_ops);


--
-- Name: authorization_userfollow_followee_id_ab3f7491; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authorization_userfollow_followee_id_ab3f7491 ON public.authorization_userfollow USING btree (followee_id);


--
-- Name: authorization_userfollow_follower_id_3efe1158; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authorization_userfollow_follower_id_3efe1158 ON public.authorization_userfollow USING btree (follower_id);


--
-- Name: authorization_usernotification_tweet_id_cdf68c4c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authorization_usernotification_tweet_id_cdf68c4c ON public.authorization_usernotification USING btree (tweet_id);


--
-- Name: authorization_usernotification_user_id_28a9c047; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authorization_usernotification_user_id_28a9c047 ON public.authorization_usernotification USING btree (user_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: tweets_tag_related_tweets_tag_id_54902faa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tag_related_tweets_tag_id_54902faa ON public.tweets_tag_related_tweets USING btree (tag_id);


--
-- Name: tweets_tag_related_tweets_tweet_id_dc4f8862; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tag_related_tweets_tweet_id_dc4f8862 ON public.tweets_tag_related_tweets USING btree (tweet_id);


--
-- Name: tweets_tweet_parent_id_a071850b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweet_parent_id_a071850b ON public.tweets_tweet USING btree (parent_id);


--
-- Name: tweets_tweet_text_abec9e2a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweet_text_abec9e2a ON public.tweets_tweet USING btree (text);


--
-- Name: tweets_tweet_text_abec9e2a_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweet_text_abec9e2a_like ON public.tweets_tweet USING btree (text varchar_pattern_ops);


--
-- Name: tweets_tweet_tree_id_201844c7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweet_tree_id_201844c7 ON public.tweets_tweet USING btree (tree_id);


--
-- Name: tweets_tweet_user_id_6c666125; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweet_user_id_6c666125 ON public.tweets_tweet USING btree (user_id);


--
-- Name: tweets_tweetbookmark_tweet_id_bd548e78; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweetbookmark_tweet_id_bd548e78 ON public.tweets_tweetbookmark USING btree (tweet_id);


--
-- Name: tweets_tweetbookmark_user_id_ffe65887; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweetbookmark_user_id_ffe65887 ON public.tweets_tweetbookmark USING btree (user_id);


--
-- Name: tweets_tweetlike_tweet_id_4aeb48c5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweetlike_tweet_id_4aeb48c5 ON public.tweets_tweetlike USING btree (tweet_id);


--
-- Name: tweets_tweetlike_user_id_852fc1c4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweetlike_user_id_852fc1c4 ON public.tweets_tweetlike USING btree (user_id);


--
-- Name: tweets_tweetretweet_tweet_id_11e15383; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweetretweet_tweet_id_11e15383 ON public.tweets_tweetretweet USING btree (tweet_id);


--
-- Name: tweets_tweetretweet_user_id_a4b89d21; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweetretweet_user_id_a4b89d21 ON public.tweets_tweetretweet USING btree (user_id);


--
-- Name: tweets_tweetusers_parents_tweet_id_d39e0496; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweetusers_parents_tweet_id_d39e0496 ON public.tweets_tweetusers_parents USING btree (tweet_id);


--
-- Name: tweets_tweetusers_parents_user_id_e711d87a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tweets_tweetusers_parents_user_id_e711d87a ON public.tweets_tweetusers_parents USING btree (user_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authorization_customuser_user_permissions authorization_custom_customuser_id_4937d13e_fk_authoriza; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser_user_permissions
    ADD CONSTRAINT authorization_custom_customuser_id_4937d13e_fk_authoriza FOREIGN KEY (customuser_id) REFERENCES public.authorization_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authorization_customuser_groups authorization_custom_customuser_id_da62a643_fk_authoriza; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser_groups
    ADD CONSTRAINT authorization_custom_customuser_id_da62a643_fk_authoriza FOREIGN KEY (customuser_id) REFERENCES public.authorization_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authorization_customuser_groups authorization_custom_group_id_0b5b1325_fk_auth_grou; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser_groups
    ADD CONSTRAINT authorization_custom_group_id_0b5b1325_fk_auth_grou FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authorization_customuser_user_permissions authorization_custom_permission_id_2f0f60f9_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_customuser_user_permissions
    ADD CONSTRAINT authorization_custom_permission_id_2f0f60f9_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authorization_userfollow authorization_userfo_followee_id_ab3f7491_fk_authoriza; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_userfollow
    ADD CONSTRAINT authorization_userfo_followee_id_ab3f7491_fk_authoriza FOREIGN KEY (followee_id) REFERENCES public.authorization_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authorization_userfollow authorization_userfo_follower_id_3efe1158_fk_authoriza; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_userfollow
    ADD CONSTRAINT authorization_userfo_follower_id_3efe1158_fk_authoriza FOREIGN KEY (follower_id) REFERENCES public.authorization_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authorization_usernotification authorization_userno_tweet_id_cdf68c4c_fk_tweets_tw; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_usernotification
    ADD CONSTRAINT authorization_userno_tweet_id_cdf68c4c_fk_tweets_tw FOREIGN KEY (tweet_id) REFERENCES public.tweets_tweet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authorization_usernotification authorization_userno_user_id_28a9c047_fk_authoriza; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authorization_usernotification
    ADD CONSTRAINT authorization_userno_user_id_28a9c047_fk_authoriza FOREIGN KEY (user_id) REFERENCES public.authorization_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_authoriza; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_authoriza FOREIGN KEY (user_id) REFERENCES public.authorization_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tweets_tag_related_tweets tweets_tag_related_tweets_tag_id_54902faa_fk_tweets_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tag_related_tweets
    ADD CONSTRAINT tweets_tag_related_tweets_tag_id_54902faa_fk_tweets_tag_id FOREIGN KEY (tag_id) REFERENCES public.tweets_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tweets_tag_related_tweets tweets_tag_related_tweets_tweet_id_dc4f8862_fk_tweets_tweet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tag_related_tweets
    ADD CONSTRAINT tweets_tag_related_tweets_tweet_id_dc4f8862_fk_tweets_tweet_id FOREIGN KEY (tweet_id) REFERENCES public.tweets_tweet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tweets_tweet tweets_tweet_parent_id_a071850b_fk_tweets_tweet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweet
    ADD CONSTRAINT tweets_tweet_parent_id_a071850b_fk_tweets_tweet_id FOREIGN KEY (parent_id) REFERENCES public.tweets_tweet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tweets_tweet tweets_tweet_user_id_6c666125_fk_authorization_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweet
    ADD CONSTRAINT tweets_tweet_user_id_6c666125_fk_authorization_customuser_id FOREIGN KEY (user_id) REFERENCES public.authorization_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tweets_tweetbookmark tweets_tweetbookmark_tweet_id_bd548e78_fk_tweets_tweet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetbookmark
    ADD CONSTRAINT tweets_tweetbookmark_tweet_id_bd548e78_fk_tweets_tweet_id FOREIGN KEY (tweet_id) REFERENCES public.tweets_tweet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tweets_tweetbookmark tweets_tweetbookmark_user_id_ffe65887_fk_authoriza; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetbookmark
    ADD CONSTRAINT tweets_tweetbookmark_user_id_ffe65887_fk_authoriza FOREIGN KEY (user_id) REFERENCES public.authorization_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tweets_tweetlike tweets_tweetlike_tweet_id_4aeb48c5_fk_tweets_tweet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetlike
    ADD CONSTRAINT tweets_tweetlike_tweet_id_4aeb48c5_fk_tweets_tweet_id FOREIGN KEY (tweet_id) REFERENCES public.tweets_tweet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tweets_tweetlike tweets_tweetlike_user_id_852fc1c4_fk_authoriza; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetlike
    ADD CONSTRAINT tweets_tweetlike_user_id_852fc1c4_fk_authoriza FOREIGN KEY (user_id) REFERENCES public.authorization_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tweets_tweetretweet tweets_tweetretweet_tweet_id_11e15383_fk_tweets_tweet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetretweet
    ADD CONSTRAINT tweets_tweetretweet_tweet_id_11e15383_fk_tweets_tweet_id FOREIGN KEY (tweet_id) REFERENCES public.tweets_tweet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tweets_tweetretweet tweets_tweetretweet_user_id_a4b89d21_fk_authoriza; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetretweet
    ADD CONSTRAINT tweets_tweetretweet_user_id_a4b89d21_fk_authoriza FOREIGN KEY (user_id) REFERENCES public.authorization_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tweets_tweetusers_parents tweets_tweetusers_pa_user_id_e711d87a_fk_authoriza; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetusers_parents
    ADD CONSTRAINT tweets_tweetusers_pa_user_id_e711d87a_fk_authoriza FOREIGN KEY (user_id) REFERENCES public.authorization_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tweets_tweetusers_parents tweets_tweetusers_parents_tweet_id_d39e0496_fk_tweets_tweet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweets_tweetusers_parents
    ADD CONSTRAINT tweets_tweetusers_parents_tweet_id_d39e0496_fk_tweets_tweet_id FOREIGN KEY (tweet_id) REFERENCES public.tweets_tweet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

