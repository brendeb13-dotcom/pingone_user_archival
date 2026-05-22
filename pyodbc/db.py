import psycopg2
import os

def get_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            dbname=os.environ.get("DB_NAME", "offboarding_user_db"),
            user=os.environ.get("DB_USER", "offboarding_user"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST", "localhost"),
            port=os.environ.get("DB_PORT", "5432")
        )
        return connection
    except psycopg2.OperationalError as e:
        # This will catch errors like wrong password, host, etc.
        print(f"Error connecting to PostgreSQL database: {e}")
        raise