#!/bin/bash

# This script sets up the PostgreSQL database by executing the SQL scripts.
# Make sure you have created the database and user first.
#
# Set the PGPASSWORD environment variable before running this script:
# export PGPASSWORD='YourStrongPassword'

DB_NAME="offboarding_user_db"
DB_USER="offboarding_user"
SQL_DIR="/home/vboxuser/Code_To_Share/SQL"

echo "--- Starting Database Setup for PostgreSQL ---"

# List of SQL files to execute in order
SQL_FILES=(
  "tbl_AlphaUserDetails.sql"
  "tbl_ArchivedUserDetails.sql"
  "tbl_JobLogs.sql"
  "sp_insert_alpha_details.sql"
  "sp_archive_deleted_users.sql"
)

#!/bin/bash

# This script sets up the PostgreSQL database by executing the SQL scripts.
# Make sure you have created the database and user first.
#
# Set the PGPASSWORD environment variable before running this script:
# export PGPASSWORD='YourStrongPassword'

DB_NAME="offboarding_user_db"
DB_USER="offboarding_user"
SQL_DIR="/home/vboxuser/Code_To_Share/SQL"

echo "--- Starting Database Setup for PostgreSQL ---"

# List of SQL files to execute in order
SQL_FILES=(
  "tbl_AlphaUserDetails.sql"
  "tbl_ArchivedUserDetails.sql"
  "tbl_JobLogs.sql"
  "sp_insert_alpha_details.sql"
  "sp_archive_deleted_users.sql"
)

# Loop through the SQL files and execute them
for sql_file in "${SQL_FILES[@]}"; do
  echo "Executing $sql_file..."
  # The -v ON_ERROR_STOP=1 flag ensures that the script will exit if any SQL error occurs.
  # The -f flag is used to specify the file to execute.
  psql -v ON_ERROR_STOP=1 -h localhost -d "$DB_NAME" -U "$DB_USER" -f "$SQL_DIR/$sql_file"
  
  if [ $? -eq 0 ]; then
    echo "Successfully executed $sql_file."
  else
    echo "ERROR: Failed to execute $sql_file."
    # Exit the script if any command fails
    exit 1
  fi
done

echo "--- Database Setup Complete ---"
echo "You can now unset the PGPASSWORD variable: unset PGPASSWORD"
    echo "ERROR: Failed to execute $sql_file."
    # Exit the script if any command fails
    exit 1
  fi
done

echo "--- Database Setup Complete ---"
echo "You can now unset the PGPASSWORD variable: unset PGPASSWORD"