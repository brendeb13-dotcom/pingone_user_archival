-- Drop the table if it exists to ensure a clean slate.
DROP TABLE IF EXISTS public.tbl_joblogs;

-- This table stores the history and results of CSV processing jobs, both manual and automated.
-- The schema is based on the output of `pg_dump` to ensure it is up-to-date.
CREATE TABLE public.tbl_joblogs (
    job_id SERIAL PRIMARY KEY,
    job_type character varying(255),
    run_timestamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(50),
    message text,
    records_inserted integer,
    records_updated integer,
    records_archived integer,
    source_file_name character varying(255)
);

-- Set the owner of the table.
ALTER TABLE public.tbl_joblogs OWNER TO offboarding_user;