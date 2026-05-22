-- Table to store the history and results of CSV processing jobs.
CREATE TABLE IF NOT EXISTS tbl_JobLogs (
    job_id SERIAL PRIMARY KEY,
    job_type VARCHAR(50) NOT NULL, -- 'Manual' or 'Automatic'
    run_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR(50) NOT NULL, -- 'Success' or 'Failure'
    message TEXT,
    records_inserted INTEGER DEFAULT 0,
    records_updated INTEGER DEFAULT 0,
    records_archived INTEGER DEFAULT 0,
    source_file_name VARCHAR(255)
);
