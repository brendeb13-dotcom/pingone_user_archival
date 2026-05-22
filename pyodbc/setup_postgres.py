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

        # SQL to create tbl_AlphaUserDetails
        create_alpha_users_table = """
        CREATE TABLE IF NOT EXISTS tbl_AlphaUserDetails (
            UserID VARCHAR(255) PRIMARY KEY,
            UserName VARCHAR(255),
            FirstName VARCHAR(255),
            LastName VARCHAR(255),
            UserType VARCHAR(255),
            Email VARCHAR(255),
            Manager VARCHAR(255),
            is_AD BOOLEAN,
            is_SA BOOLEAN,
            created_on TIMESTAMP,
            last_login_timestamp TIMESTAMP
        );
        """

        # SQL to create tbl_JobLogs
        create_job_logs_table = """
        CREATE TABLE IF NOT EXISTS tbl_JobLogs (
            job_id SERIAL PRIMARY KEY,
            job_type VARCHAR(255),
            run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50),
            message TEXT,
            records_inserted INTEGER,
            records_updated INTEGER,
            records_archived INTEGER,
            source_file_name VARCHAR(255)
        );
        """

        # SQL to create tbl_ArchivedAlphaUserDetails
        create_archived_alpha_users_table = """
        CREATE TABLE IF NOT EXISTS tbl_ArchivedAlphaUserDetails (
            archive_id SERIAL PRIMARY KEY,
            archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UserID VARCHAR(255),
            UserName VARCHAR(255),
            FirstName VARCHAR(255),
            LastName VARCHAR(255),
            UserType VARCHAR(255),
            Email VARCHAR(255),
            Manager VARCHAR(255),
            is_AD BOOLEAN,
            is_SA BOOLEAN,
            created_on TIMESTAMP,
            last_login_timestamp TIMESTAMP
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