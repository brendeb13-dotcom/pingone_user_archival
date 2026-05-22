import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PaginationComponent } from '../../shared/pagination/pagination.component';
import { ExportService } from '../../shared/export/export.service';
import { FormsModule } from '@angular/forms';
import { PingoneApiService } from '../../Core/api/pingone-api.service';


@Component({
  standalone: true,
  imports: [PaginationComponent, FormsModule, CommonModule],
  templateUrl: './offboarding.html',
  styleUrl: './offboarding.css'
})
export default class OffboardingComponent implements OnInit {
  users: any[] = [];
  page = 0; size = 10; total = 0;
  search = ''; sortField = 'username'; sortDir: 'asc' | 'desc' = 'asc';


  constructor(private api: PingoneApiService, private exporter: ExportService) { }


  ngOnInit() { this.load(); }


  load() {
    this.api.offboarding({
      filter: 'lifecycleStatus eq "OFFBOARDING"',
      page: this.page,
      size: this.size,
      search: this.search,
      sort: `${this.sortField},${this.sortDir}`
    }).subscribe((res: any) => {
      this.users = res._embedded?.users || [];
      this.total = res.count || 0;
    });
  }


  sort(f: string) {
    this.sortDir = this.sortField === f && this.sortDir === 'asc' ? 'desc' : 'asc';
    this.sortField = f; this.load();
  }


  //export() { this.exporter.excel(this.users, 'offboarding-users'); }
}