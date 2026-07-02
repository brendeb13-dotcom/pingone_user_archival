import psycopg2
import os

def setup_database():
    """
    Connects to the PostgreSQL database and creates the necessary tables
    if they do not already exist.
    """
    try:
        # Use the same environment variables as the main application
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME", "offboarding_user_db"),
            user=os.environ.get("DB_USER", "offboarding_user"),
            password=os.environ.get("DB_PASSWORD", "genic"), # IMPORTANT: Replace with your password if needed
            host=os.environ.get("DB_HOST", "localhost"),
            port=os.environ.get("DB_PORT", "5432")
        )
        cursor = conn.cursor()

        # SQL to create tbl_AlphaUserDetails based on the current schema
        create_alpha_users_table = """
        CREATE TABLE IF NOT EXISTS public.tbl_alphauserdetails (
            _id text NOT NULL PRIMARY KEY,
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
        """

        # SQL to create tbl_JobLogs based on the current schema
        create_job_logs_table = """
        CREATE TABLE IF NOT EXISTS public.tbl_joblogs (
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
        """

        # SQL to create tbl_ArchivedAlphaUserDetails
        # NOTE: The schema for this table was not provided in the pg_dump.
        # SQL to create tbl_ArchivedAlphaUserDetails as a mirror of the main table
        create_archived_alpha_users_table = """
        CREATE TABLE IF NOT EXISTS public.tbl_archivedalphauserdetails (
            archived_at timestamp with time zone DEFAULT now(),
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
            last_modified timestamp with time zone,
            operation_type character varying(10),
            PRIMARY KEY (_id, archived_at)
        );
        """

        # Execute the table creation statements
        cursor.execute(create_alpha_users_table)
        print("Table 'tbl_AlphaUserDetails' created or already exists.")
        
        cursor.execute(create_job_logs_table)
        print("Table 'tbl_JobLogs' created or already exists.")

        cursor.execute(create_archived_alpha_users_table)
        print("Table 'tbl_ArchivedAlphaUserDetails' created or already exists.")

        # Commit the changes
        conn.commit()

        cursor.close()
        conn.close()
        print("Database setup completed successfully!")

    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        print("Please ensure PostgreSQL is running and the credentials are correct.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    setup_database()