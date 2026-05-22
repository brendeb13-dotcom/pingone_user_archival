import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PaginationComponent } from '../../shared/pagination/pagination.component';
import { RealtimeService } from '../../Core/api/realtime.service';
import { PingoneApiService } from '../../Core/api/pingone-api.service';


@Component({
  standalone: true,
  imports: [PaginationComponent, CommonModule],
  templateUrl: './scheduled-jobs.html',
  styleUrl: './scheduled-jobs.css'
})
export default class ScheduledJobsComponent implements OnInit {
  jobs: any[] = [];
  page = 0; size = 10; total = 0;
  sortField = 'name'; sortDir: 'asc' | 'desc' = 'asc';


  constructor(private api: PingoneApiService, private realtime: RealtimeService) { }


  ngOnInit() {
    this.load();
    const sse = this.realtime.connect();
    sse.onmessage = e => {
      const update = JSON.parse(e.data);
      const job = this.jobs.find(j => j.id === update.id);
      if (job) job.status = update.status;
    };
  }


  load() {
    this.api.getAlphaUser().subscribe((res: any) => {
      console.log('Alpha Users:', res);
      this.jobs = res._embedded?.jobs || [];
      this.total = res.count || 0;
    });
  }


  sort(f: string) {
    this.sortDir = this.sortField === f && this.sortDir === 'asc' ? 'desc' : 'asc';
    this.sortField = f; this.load();
  }
}