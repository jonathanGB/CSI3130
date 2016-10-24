DROP TABLE IF EXISTS public.owns;
DROP TABLE IF EXISTS public.account;
DROP TABLE IF EXISTS public.client;
DROP TABLE IF EXISTS public.branch;



CREATE TABLE public.branch
(
  "branch-number" integer NOT NULL,
  "branch-name" character varying(30),
  city character varying(30),
  CONSTRAINT branch_pkey PRIMARY KEY ("branch-number")
);

CREATE TABLE public.client
(
  "client-number" integer NOT NULL,
  lastname character varying(30),
  firstname character varying(30),
  "marital-status" character varying(20),
  "postal-code" character varying(7),
  phone character(10),
  city character varying(30),
  CONSTRAINT client_pkey PRIMARY KEY ("client-number")
);

CREATE TABLE public.account (
  "acc-number" integer NOT NULL,
  "dollar-balance" money,
  "branch-number" integer,
  CONSTRAINT "Account_pkey" PRIMARY KEY ("acc-number"),
  CONSTRAINT "account_branch-number_fkey" FOREIGN KEY ("branch-number")
      REFERENCES public.branch ("branch-number") MATCH SIMPLE
);

CREATE TABLE public.owns
(
  "client-number" integer NOT NULL,
  "acc-number" integer NOT NULL,
  CONSTRAINT owns_pkey PRIMARY KEY ("client-number", "acc-number"),
  CONSTRAINT "owns_acc-number_fkey" FOREIGN KEY ("acc-number")
      REFERENCES public.account ("acc-number") MATCH SIMPLE,
  CONSTRAINT "owns_client-number_fkey" FOREIGN KEY ("client-number")
      REFERENCES public.client ("client-number") MATCH SIMPLE
)
