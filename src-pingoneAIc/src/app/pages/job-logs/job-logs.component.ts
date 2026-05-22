import { Component, OnInit, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { JobLog } from '../../models/job-log.model';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';

@Component({
  selector: 'app-job-logs',
  standalone: true,
  imports: [CommonModule, TableModule, TagModule],
  templateUrl: './job-logs.component.html',
  styleUrl: './job-logs.component.css'
})
export class JobLogsComponent implements OnInit {
  private http = inject(HttpClient);
  jobLogs = signal<JobLog[]>([]);
  loading = signal(true);

  ngOnInit(): void {
    this.loadJobLogs();
  }

  loadJobLogs(): void {
    this.loading.set(true);
    this.http.get<JobLog[]>('/api/job-logs').subscribe({
      next: (data) => {
        this.jobLogs.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('Failed to fetch job logs:', err);
        this.loading.set(false);
      }
    });
  }

  getSeverity(status: string): 'success' | 'warn' | 'danger' {
    switch (status) {
      case 'Success':
        return 'success';
      case 'In Progress':
        return 'warn';
      case 'Failure':
        return 'danger';
      default:
        return 'danger';
    }
  }
}