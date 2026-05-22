export interface Job {
  _id: string;
  enabled: boolean;
  type: string;
  schedule: string;
  nextRunDate?: string;
  previousRunDate?: string;
}
