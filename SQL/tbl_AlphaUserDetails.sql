-- Drop the table if it exists to ensure a clean slate.
DROP TABLE IF EXISTS public.tbl_alphauserdetails;

-- This table stores the comprehensive details of users, mirroring the structure
-- from the source CSV file. It serves as the primary repository for active user data.
-- The schema is based on the output of `pg_dump` to ensure it is up-to-date.
CREATE TABLE public.tbl_alphauserdetails (
    _id text NOT NULL,
    _rev text,
    custom_regcompanyname text,
    frunindexedstring1 text,
    frunindexedstring2 text,
    frunindexedstring3 text,
    frunindexedstring4 text,
    frunindexedstring5 text,
    frindexedstring11 text,
    frindexedstring12 text,
    frindexedstring10 text,
    frindexedstring19 text,
    frindexedstring17 text,
    frindexedstring18 text,
    frindexedstring15 text,
    frindexedstring16 text,
    frindexedstring13 text,
    frindexedstring14 text,
    givenname text,
    frindexedstring20 text,
    telephonenumber text,
    city text,
    displayname text,
    accountstatus text,
    sn text,
    frunindexeddate1 timestamp without time zone,
    frindexedstring9 text,
    frindexedstring8 text,
    frindexedstring7 text,
    frindexedstring6 text,
    passwordlastchangedtime timestamp without time zone,
    country text,
    mail text,
    frindexeddate5 timestamp without time zone,
    frindexeddate4 timestamp without time zone,
    frindexeddate3 timestamp without time zone,
    frindexedstring5 text,
    frindexedstring4 text,
    frindexedstring3 text,
    frindexedstring2 text,
    frindexedstring1 text,
    frunindexedinteger3 integer,
    frunindexedinteger2 integer,
    frunindexedinteger1 integer,
    description text,
    frindexedinteger4 integer,
    frindexedinteger3 integer,
    frindexedinteger2 integer,
    frindexedinteger1 integer,
    frindexedinteger5 integer,
    username text,
    frindexeddate2 timestamp without time zone,
    frindexeddate1 timestamp without time zone,
    last_modified timestamp with time zone DEFAULT now(),
    operation_type character varying(10)
);

-- Set the owner of the table.
ALTER TABLE public.tbl_alphauserdetails OWNER TO offboarding_user;

-- Add the primary key constraint.
ALTER TABLE ONLY public.tbl_alphauserdetails
    ADD CONSTRAINT tbl_alphauserdetails_pkey PRIMARY KEY (_id);