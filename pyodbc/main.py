import os
import io
import pandas as pd
import psycopg2
import psycopg2.extras
from psycopg2.extras import Json
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from datetime import datetime
from auth import router as auth_router

# --- Database Connection ---
def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "pingone"),
        user=os.environ.get("DB_USER", "ping"),
        password=os.environ.get("DB_PASSWORD", "ping"),
    )

def get_db():
    """Dependency function to get a database connection."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            database=os.environ.get("DB_NAME", "pingone"),
            user=os.environ.get("DB_USER", "ping"),
            password=os.environ.get("DB_PASSWORD", "ping"),
        )
        yield conn
    finally:
        if conn is not None:
            conn.close()

# --- Pydantic Models ---
from models import AlphaUser, JobLog

class ActivityTrend(BaseModel):
    date: str
    inserted: int
    updated: int
    archived: int

class DashboardUser(BaseModel):
    name: str | None
    email: str | None
    country: str | None
    accountstatus: str | None
    operation_type: str | None

class DashboardCard(BaseModel):
    count: int
    users: List[DashboardUser]

class DashboardData(BaseModel):
    employee: DashboardCard
    contractor: DashboardCard
    other: DashboardCard
    total_users: int
    active_users: int
    inactive_users: int
    other_status_users: int
    add_ops: int
    update_ops: int
    today_count: int
    week_count: int
    month_count: int

# --- FastAPI App ---
app = FastAPI()

# Configure CORS
# In production, this should be set to the specific frontend domain.
# e.g., "https://your-app.com"
allowed_origins_str = os.environ.get("ALLOWED_ORIGINS")
if not allowed_origins_str:
    print("WARNING: ALLOWED_ORIGINS environment variable not set. CORS will not be configured, which is insecure for development but necessary for production behind a reverse proxy.")
    allowed_origins = []
else:
    allowed_origins = allowed_origins_str.split(",")
    if "*" in allowed_origins:
        print("WARNING: Using a wildcard ('*') for ALLOWED_ORIGINS is insecure and not recommended for production.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/api/dashboard-data", response_model=DashboardData)
def get_dashboard_data(db=Depends(get_db)):
    try:
        with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            # --- Fetch user details for cards ---
            cursor.execute("""
                SELECT
                    frindexedstring2 as user_type,
                    frindexedstring18 as name,
                    frindexedstring6 as email,
                    country,
                    accountstatus,
                    operation_type
                FROM tbl_alphauserdetails
            """)
            all_users = cursor.fetchall()

            # --- Fetch aggregated stats in a separate query ---
            cursor.execute("""
                SELECT
                    COUNT(*) FILTER (WHERE last_modified >= date_trunc('day', NOW())) AS today_count,
                    COUNT(*) FILTER (WHERE last_modified >= date_trunc('week', NOW())) AS week_count,
                    COUNT(*) FILTER (WHERE last_modified >= date_trunc('month', NOW())) AS month_count,
                    COUNT(*) FILTER (WHERE frindexedstring1 = 'ADD') AS add_ops,
                    COUNT(*) FILTER (WHERE frindexedstring1 = 'UPDATE') AS update_ops
                FROM tbl_alphauserdetails
            """)
            stats = cursor.fetchone()

            # Initialize data structures
            data = {
                "employee": {"count": 0, "users": []},
                "contractor": {"count": 0, "users": []},
                "other": {"count": 0, "users": []},
                "total_users": len(all_users),
                "active_users": 0,
                "inactive_users": 0,
                "other_status_users": 0,
                "add_ops": stats['add_ops'] or 0,
                "update_ops": stats['update_ops'] or 0,
                "today_count": stats['today_count'] or 0,
                "week_count": stats['week_count'] or 0,
                "month_count": stats['month_count'] or 0,
            }

            # Process each user for user-specific cards
            for user in all_users:
                user_card = DashboardUser(
                    name=user['name'],
                    email=user['email'],
                    country=user['country'],
                    accountstatus=user['accountstatus'],
                    operation_type=user['operation_type']
                )

                # Categorize by user type
                user_type = (user['user_type'] or 'other').lower().strip()
                if user_type == 'employee':
                    data["employee"]["users"].append(user_card)
                elif user_type == 'contractor':
                    data["contractor"]["users"].append(user_card)
                else:
                    data["other"]["users"].append(user_card)

                # Categorize by account status
                status = (user['accountstatus'] or '').lower()
                if status == 'active':
                    data["active_users"] += 1
                elif status == 'inactive':
                    data["inactive_users"] += 1
                else:
                    data["other_status_users"] += 1

            # Set counts after processing all users
            data["employee"]["count"] = len(data["employee"]["users"])
            data["contractor"]["count"] = len(data["contractor"]["users"])
            data["other"]["count"] = len(data["other"]["users"])

            return DashboardData(**data)

    except Exception as e:
        print(f"ERROR fetching dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/users/timely", response_model=List[DashboardUser])
def get_timely_users(period: str, db=Depends(get_db)):
    """
    Fetches users based on the last_modified timestamp for a given period.
    Valid periods are 'today', 'week', 'month'.
    """
    if period not in ['today', 'week', 'month']:
        raise HTTPException(status_code=400, detail="Invalid period specified. Use 'today', 'week', or 'month'.")

    try:
        with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = f"""
                SELECT
                    frindexedstring18 as name,
                    frindexedstring6 as email,
                    country,
                    accountstatus,
                    operation_type
                FROM tbl_alphauserdetails
                WHERE last_modified >= date_trunc('{period}', NOW())
            """
            cursor.execute(query)
            users = [DashboardUser(**row) for row in cursor.fetchall()]
            return users
    except Exception as e:
        print(f"ERROR fetching timely users for period '{period}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


# --- Helper Functions ---
def log_job(db, job_type: str, status: str, message: str, inserted: int, updated: int, archived: int, source_file: str):
    """
    Logs a job record to the database within the current transaction.
    It does NOT commit or rollback.
    """
    try:
        cursor = db.cursor()
        query = """
            INSERT INTO tbl_JobLogs (job_type, run_timestamp, status, message, records_inserted, records_updated, records_archived, source_file_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Note: run_timestamp is generated by the database default value (NOW())
        params = (
            job_type, datetime.now(), status, message,
            inserted, updated, archived,
            source_file
        )
        cursor.execute(query, params)
        # DO NOT COMMIT HERE. The calling function manages the transaction.
    except Exception as e:
        # If logging itself fails, we print a critical error.
        # We don't rollback, as the main exception handler will do that.
        print(f"CRITICAL: Failed to log job status to database. Error: {e}")


def process_csv_and_reconcile(db, contents, filename):
    """
    Processes a CSV file, upserts data, and deletes old records within a single transaction.
    This function is designed to be called from an endpoint that manages the transaction.
    It returns counts of inserted, updated, deleted, and failed records.
    """
    df = pd.read_csv(io.BytesIO(contents))
    df.columns = df.columns.str.strip()
    df = df.astype(object).where(pd.notna(df), None) # Convert numpy.nan to None

    cursor = db.cursor()

    try:
        # --- Get existing user IDs from the database ---
        cursor.execute("SELECT _id FROM tbl_alphauserdetails")
        db_user_ids = {row[0] for row in cursor.fetchall()}

        if '_id' not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain an '_id' column.")

        csv_user_ids = set(df['_id'].astype(str))

        # --- Upsert users from the CSV, with row-level error handling ---
        inserted_count = 0
        updated_count = 0
        failed_count = 0

        for _, row in df.iterrows():
            try:
                user_id = str(row['_id'])
                user_data = row.to_dict()

                # Determine operation type
                if user_id in db_user_ids:
                    updated_count += 1
                    op_type = 'Updated'
                else:
                    inserted_count += 1
                    op_type = 'Inserted'
                user_data['operation_type'] = op_type


                # --- Robust Date Parsing ---
                for date_col in ['frUnindexedDate1', 'passwordLastChangedTime', 'frIndexedDate5', 'frIndexedDate4', 'frIndexedDate3', 'frIndexedDate2', 'frIndexedDate1']:
                    if user_data.get(date_col) is not None:
                        try:
                            user_data[date_col] = pd.to_datetime(user_data[date_col])
                        except (ValueError, TypeError):
                            user_data[date_col] = None # Set to null if parsing fails

                # --- Prepare parameters for SQL ---
                all_cols = [
                    '_id', '_rev', 'custom_RegCompanyName', 'frUnindexedString1', 'frUnindexedString2', 'frUnindexedString3', 'frUnindexedString4', 'frUnindexedString5',
                    'frIndexedString11', 'frIndexedString12', 'frIndexedString10', 'frIndexedString19', 'frIndexedString17', 'frIndexedString18', 'frIndexedString15',
                    'frIndexedString16', 'frIndexedString13', 'frIndexedString14', 'givenName', 'frIndexedString20', 'telephoneNumber', 'city', 'displayName',
                    'accountStatus', 'sn', 'frUnindexedDate1', 'frIndexedString9', 'frIndexedString8', 'frIndexedString7', 'frIndexedString6', 'passwordLastChangedTime',
                    'country', 'mail', 'frIndexedDate5', 'frIndexedDate4', 'frIndexedDate3', 'frIndexedString5', 'frIndexedString4', 'frIndexedString3', 'frIndexedString2',
                    'frIndexedString1', 'frUnindexedInteger3', 'frUnindexedInteger2', 'frUnindexedInteger1', 'description', 'frIndexedInteger4', 'frIndexedInteger3',
                    'frIndexedInteger2', 'frIndexedInteger1', 'frIndexedInteger5', 'userName', 'frIndexedDate2', 'frIndexedDate1', 'operation_type'
                ]
                params = [user_data.get(col) for col in all_cols]

                upsert_sql = """
                INSERT INTO tbl_alphauserdetails (
                    _id, _rev, custom_RegCompanyName, frUnindexedString1, frUnindexedString2, frUnindexedString3, frUnindexedString4, frUnindexedString5,
                    frIndexedString11, frIndexedString12, frIndexedString10, frIndexedString19, frIndexedString17, frIndexedString18, frIndexedString15,
                    frIndexedString16, frIndexedString13, frIndexedString14, givenName, frIndexedString20, telephoneNumber, city, displayName,
                    accountStatus, sn, frUnindexedDate1, frIndexedString9, frIndexedString8, frIndexedString7, frIndexedString6, passwordLastChangedTime,
                    country, mail, frIndexedDate5, frIndexedDate4, frIndexedDate3, frIndexedString5, frIndexedString4, frIndexedString3, frIndexedString2,
                    frIndexedString1, frUnindexedInteger3, frUnindexedInteger2, frUnindexedInteger1, description, frIndexedInteger4, frIndexedInteger3,
                    frIndexedInteger2, frIndexedInteger1, frIndexedInteger5, userName, frIndexedDate2, frIndexedDate1, operation_type
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (_id) DO UPDATE SET
                    _rev = EXCLUDED._rev, custom_RegCompanyName = EXCLUDED.custom_RegCompanyName, frUnindexedString1 = EXCLUDED.frUnindexedString1,
                    frUnindexedString2 = EXCLUDED.frUnindexedString2, frUnindexedString3 = EXCLUDED.frUnindexedString3, frUnindexedString4 = EXCLUDED.frUnindexedString4,
                    frUnindexedString5 = EXCLUDED.frUnindexedString5, frIndexedString11 = EXCLUDED.frIndexedString11, frIndexedString12 = EXCLUDED.frIndexedString12,
                    frIndexedString10 = EXCLUDED.frIndexedString10, frIndexedString19 = EXCLUDED.frIndexedString19, frIndexedString17 = EXCLUDED.frIndexedString17,
                    frIndexedString18 = EXCLUDED.frIndexedString18, frIndexedString15 = EXCLUDED.frIndexedString15, frIndexedString16 = EXCLUDED.frIndexedString16,
                    frIndexedString13 = EXCLUDED.frIndexedString13, frIndexedString14 = EXCLUDED.frIndexedString14, givenName = EXCLUDED.givenName,
                    frIndexedString20 = EXCLUDED.frIndexedString20, telephoneNumber = EXCLUDED.telephoneNumber, city = EXCLUDED.city,
                    displayName = EXCLUDED.displayName, accountStatus = EXCLUDED.accountStatus, sn = EXCLUDED.sn, frUnindexedDate1 = EXCLUDED.frUnindexedDate1,
                    frIndexedString9 = EXCLUDED.frIndexedString9, frIndexedString8 = EXCLUDED.frIndexedString8, frIndexedString7 = EXCLUDED.frIndexedString7,
                    frIndexedString6 = EXCLUDED.frIndexedString6, passwordLastChangedTime = EXCLUDED.passwordLastChangedTime, country = EXCLUDED.country,
                    mail = EXCLUDED.mail, frIndexedDate5 = EXCLUDED.frIndexedDate5, frIndexedDate4 = EXCLUDED.frIndexedDate4, frIndexedDate3 = EXCLUDED.frIndexedDate3,
                    frIndexedString5 = EXCLUDED.frIndexedString5, frIndexedString4 = EXCLUDED.frIndexedString4, frIndexedString3 = EXCLUDED.frIndexedString3,
                    frIndexedString2 = EXCLUDED.frIndexedString2, frIndexedString1 = EXCLUDED.frIndexedString1, frUnindexedInteger3 = EXCLUDED.frUnindexedInteger3,
                    frUnindexedInteger2 = EXCLUDED.frUnindexedInteger2, frUnindexedInteger1 = EXCLUDED.frUnindexedInteger1, description = EXCLUDED.description,
                    frIndexedInteger4 = EXCLUDED.frIndexedInteger4, frIndexedInteger3 = EXCLUDED.frIndexedInteger3, frIndexedInteger2 = EXCLUDED.frIndexedInteger2,
                    frIndexedInteger1 = EXCLUDED.frIndexedInteger1, frIndexedInteger5 = EXCLUDED.frIndexedInteger5, userName = EXCLUDED.userName,
                    frIndexedDate2 = EXCLUDED.frIndexedDate2, frIndexedDate1 = EXCLUDED.frIndexedDate1,
                    operation_type = EXCLUDED.operation_type,
                    last_modified = NOW();
                """
                cursor.execute(upsert_sql, params)

            except Exception as row_error:
                failed_count += 1
                print(f"Warning: Failed to process row for UserID {row.get('_id', 'N/A')}. Error: {row_error}")

        # --- Archive users not in the CSV ---
        users_to_archive = db_user_ids - csv_user_ids
        archived_count = 0
        if users_to_archive:
            for user_id in users_to_archive:
                try:
                    # Call the stored procedure for each user to be archived
                    cursor.execute("SELECT sp_archive_deleted_users(%s);", (user_id,))
                    archived_count += 1
                except Exception as e:
                    # If a single user fails, we can log it and continue
                    print(f"Warning: Failed to archive user with ID {user_id}. Error: {e}")

        return {
            "inserted": inserted_count,
            "updated": updated_count,
            "archived": archived_count,
            "failed": failed_count
        }

    finally:
        cursor.close()



# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "PingOne User Management API is running."}

@app.get("/api/alpha-users", response_model=List[AlphaUser])
def get_alpha_users(db=Depends(get_db)):
    try:
        cursor = db.cursor()
        # Explicitly select and alias columns to avoid issues with leading underscores
        cursor.execute("""
            SELECT
                _id as id, _rev as rev, custom_regcompanyname, frunindexedstring1, frunindexedstring2,
                frunindexedstring3, frunindexedstring4, frunindexedstring5, frindexedstring11,
                frindexedstring12, frindexedstring10, frindexedstring19, frindexedstring17,
                frindexedstring18, frindexedstring15, frindexedstring16, frindexedstring13,
                frindexedstring14, givenname, frindexedstring20, telephonenumber, city,
                displayname, accountstatus, sn, frunindexeddate1, frindexedstring9,
                frindexedstring8, frindexedstring7, frindexedstring6, passwordlastchangedtime,
                country, mail, frindexeddate5, frindexeddate4, frindexeddate3, frindexedstring5,
                frindexedstring4, frindexedstring3, frindexedstring2, frindexedstring1,
                frunindexedinteger3, frunindexedinteger2, frunindexedinteger1, description,
                frindexedinteger4, frindexedinteger3, frindexedinteger2, frindexedinteger1,
                frindexedinteger5, username, frindexeddate2, frindexeddate1
            FROM tbl_alphauserdetails
        """)
        column_names = [desc[0] for desc in cursor.description]
        users = [AlphaUser(**dict(zip(column_names, row))) for row in cursor.fetchall()]
        return users
    except Exception as e:
        print(f"ERROR fetching alpha users: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/job-logs", response_model=List[JobLog])
def get_job_logs(db=Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tbl_joblogs ORDER BY run_timestamp DESC")
        column_names = [desc[0] for desc in cursor.description]
        logs = [JobLog(**dict(zip(column_names, row))) for row in cursor.fetchall()]
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def log_job_failure(job_type: str, source_file: str, error_message: str):
    """
    Logs a job failure in a separate transaction to ensure it's recorded
    even if the main transaction is rolled back.
    """
    conn = None
    try:
        # Use the main connection function to get a new, independent connection
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO tbl_JobLogs (job_type, run_timestamp, status, message, source_file_name)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (job_type, datetime.now(), "Failure", error_message, source_file)
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        # If logging itself fails, print a critical error to the console/system logs
        print(f"CRITICAL: Failed to log job failure to database. Error: {e}")
    finally:
        if conn:
            conn.close()


@app.post("/api/alpha-users/upload-csv")
async def upload_alpha_users_csv(file: UploadFile = File(...), db=Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")

    contents = await file.read()

    try:
        # Process the CSV and get counts within a single transaction
        result_details = process_csv_and_reconcile(db, contents, file.filename)

        # Log the successful job result before committing
        status = "Success" if result_details.get('failed', 0) == 0 else "Partial Success"
        message = f"{file.filename} processed. Inserted: {result_details['inserted']}, Updated: {result_details['updated']}, Archived: {result_details['archived']}, Failed: {result_details['failed']}"
        log_job(db, "Manual", status, message, result_details['inserted'], result_details['updated'], result_details['archived'], file.filename)

        # If processing is successful, commit the transaction
        db.commit()

        return {
            "message": f"Successfully processed {file.filename}",
            "inserted": result_details["inserted"],
            "updated": result_details["updated"],
            "archived": result_details["archived"],
            "failed": result_details["failed"]
        }
    except Exception as e:
        # If any error occurs, roll back the entire transaction
        db.rollback()

        # Log the failure in a separate transaction
        error_message = f"Failed to process {file.filename}: {str(e)}"
        log_job_failure("Manual", file.filename, error_message)

        # Log the full error for debugging
        print("--- TRANSACTION FAILED, ROLLING BACK ---")
        import traceback
        traceback.print_exc()
        print("--- END TRANSACTION FAILED ---")

        # Re-raise the exception to return a 500 error to the client
        raise HTTPException(status_code=500, detail=error_message)
        # A more robust solution would log to a file or separate service.
        log_job(db, "CSV Upload", "Failed", str(e), 0, 0, 0, file.filename)

        # Return a 500 error to the client
        raise HTTPException(status_code=500, detail=f"An error occurred during CSV processing: {e}")


@app.get("/api/activity-trend", response_model=List[ActivityTrend])
def get_activity_trend(db=Depends(get_db)):
    """
    Calculates the daily sum of inserted, updated, and archived records
    over the last 30 days.
    """
    try:
        with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = """
                SELECT
                    DATE(run_timestamp) as date,
                    SUM(records_inserted) as inserted,
                    SUM(records_updated) as updated,
                    SUM(records_archived) as archived
                FROM
                    tbl_joblogs
                WHERE
                    run_timestamp >= NOW() - INTERVAL '30 days'
                GROUP BY
                    DATE(run_timestamp)
                ORDER BY
                    date;
            """
            cursor.execute(query)

            # Format the results into the Pydantic model
            trend_data = [
                ActivityTrend(
                    date=row['date'].strftime('%Y-%m-%d'),
                    inserted=row['inserted'] or 0,
                    updated=row['updated'] or 0,
                    archived=row['archived'] or 0
                ) for row in cursor.fetchall()
            ]
            return trend_data

    except Exception as e:
        print(f"ERROR fetching activity trend data: {e}")