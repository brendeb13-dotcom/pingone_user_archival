export interface JobLog {
  job_id: number;
  job_type: string;
  run_timestamp: string;
  status: 'Success' | 'Failure' | 'In Progress';
  source_file_name: string;
  records_inserted: number;
  records_updated: number;
  records_archived: number;
  message: string;
}