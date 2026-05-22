import os
import shutil
import time
from datetime import datetime
import traceback

# It's crucial to import the functions from our existing application logic.
# This ensures we are reusing code and maintaining consistency.
from main import get_connection, process_csv_and_reconcile, log_job_failure

# --- Configuration ---
# The script will look for CSV files in this directory.
# You should place your CSV files here.
CSV_INPUT_DIR = os.path.join(os.path.dirname(__file__), "csv_input")

# After processing, files will be moved to this directory to prevent reprocessing.
ARCHIVE_DIR = os.path.join(CSV_INPUT_DIR, "archive")

def ensure_directories_exist():
    """Create the input and archive directories if they don't exist."""
    if not os.path.exists(CSV_INPUT_DIR):
        print(f"Creating input directory: {CSV_INPUT_DIR}")
        os.makedirs(CSV_INPUT_DIR)
    if not os.path.exists(ARCHIVE_DIR):
        print(f"Creating archive directory: {ARCHIVE_DIR}")
        os.makedirs(ARCHIVE_DIR)

def process_single_file(file_path):
    """
    Processes a single CSV file. This function contains the core logic for
    handling one file, including database operations and logging.
    """
    filename = os.path.basename(file_path)
    print(f"Processing file: {filename}")

    db_conn = None
    try:
        # Establish a database connection for this file.
        db_conn = get_connection()

        # Read the file content.
        with open(file_path, 'rb') as f:
            contents = f.read()

        # Use the existing reconciliation logic from main.py
        result_details = process_csv_and_reconcile(db_conn, contents, filename)

        # Log the outcome to the database.
        status = "Success" if result_details.get('failed', 0) == 0 else "Partial Success"
        message = (f"Automated processing of {filename}. "
                   f"Inserted: {result_details['inserted']}, "
                   f"Updated: {result_details['updated']}, "
                   f"Deleted: {result_details['deleted']}, "
                   f"Failed: {result_details['failed']}")

        # The log_job function from main.py requires the cursor, let's adapt
        # by creating a new log_job function for the automated process.
        log_automated_job(
            db_conn, "Automated", status, message,
            result_details['inserted'], result_details['updated'],
            result_details['deleted'], filename
        )

        # Commit the transaction to save changes and the log.
        db_conn.commit()
        print(f"Successfully processed and committed {filename}")

    except Exception as e:
        # If any error occurs, roll back the transaction.
        if db_conn:
            db_conn.rollback()

        # Log the failure using the robust failure logging function.
        error_message = f"Failed to process {filename}: {traceback.format_exc()}"
        print(error_message)
        log_job_failure("Automated", filename, str(e))

    finally:
        # Ensure the database connection is closed.
        if db_conn:
            db_conn.close()

        # Archive the file regardless of success or failure to prevent retries.
        try:
            shutil.move(file_path, os.path.join(ARCHIVE_DIR, filename))
            print(f"Archived file: {filename}")
        except Exception as e:
            print(f"CRITICAL: Failed to archive file {filename}. Error: {e}")


def log_automated_job(db, job_type, status, message, inserted, updated, archived, source_file):
    """Helper to log automated job results."""
    try:
        cursor = db.cursor()
        query = """
            INSERT INTO tbl_JobLogs (job_type, run_timestamp, status, message, records_inserted, records_updated, records_archived, source_file_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            job_type, datetime.now(), status, message,
            inserted, updated, archived,
            source_file
        )
        cursor.execute(query, params)
    except Exception as e:
        print(f"CRITICAL: Failed to log automated job status. Error: {e}")
        # We do not commit here; the calling function manages the transaction.


def log_no_files_found():
    """Logs a 'Failure' record when no files are found to process."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO tbl_JobLogs (job_type, run_timestamp, status, message, source_file_name)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = ("Automated", datetime.now(), "Failure", "No new CSV files found to process.", "N/A")
        cursor.execute(query, params)
        conn.commit()
        print("Logged 'No files found' failure message.")
    except Exception as e:
        print(f"CRITICAL: Failed to log 'no files found' status. Error: {e}")
    finally:
        if conn:
            conn.close()


def main():
    """
    Main function to run the automated CSV processor.
    """
    print("--- Starting Automated CSV Processor ---")
    ensure_directories_exist()

    # Find all CSV files in the input directory
    try:
        csv_files = [f for f in os.listdir(CSV_INPUT_DIR) if f.endswith('.csv') and os.path.isfile(os.path.join(CSV_INPUT_DIR, f))]

        if not csv_files:
            print("No new CSV files to process.")
            log_no_files_found()  # Log this event as a failure
        else:
            for filename in csv_files:
                file_path = os.path.join(CSV_INPUT_DIR, filename)
                process_single_file(file_path)
                # Add a small delay between files if needed
                time.sleep(1)

    except Exception as e:
        print(f"An unexpected error occurred during the main processing loop: {e}")

    print("--- Automated CSV Processor Finished ---")


if __name__ == "__main__":
    main()