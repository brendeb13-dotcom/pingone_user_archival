import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PingoneApiService } from '../../Core/api/pingone-api.service';
import { PaginationComponent } from '../../shared/pagination/pagination.component';
import { FormsModule } from '@angular/forms';


@Component({
  standalone: true,
  imports: [PaginationComponent, FormsModule, CommonModule],
  templateUrl: './failed-jobs.html',
  styleUrl: './failed-jobs.css'
})
export default class FailedJobsComponent implements OnInit {
  jobs: any[] = [];
  page = 0;
  size = 10;
  total = 0;
  errorType = '';

  constructor(private api: PingoneApiService) {}

  ngOnInit() {
    this.load();
  }

  load() {
    this.api.failedJobs({
      page: this.page,
      size: this.size,
      errorType: this.errorType
    }).subscribe((res: any) => {
      this.jobs = res._embedded?.jobs || [];
      this.total = res.count || 0;
    });
  }
}