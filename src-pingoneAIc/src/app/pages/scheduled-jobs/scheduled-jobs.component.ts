import { Component, OnInit, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { AlphaUser } from '../../models/alpha-user.model';

import { FormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';

// PrimeNG Modules
import { TableModule } from 'primeng/table';
import { InputTextModule } from 'primeng/inputtext';
import { IconFieldModule } from 'primeng/iconfield';
import { InputIconModule } from 'primeng/inputicon';


interface Column {
  field: string;
  header: string;
}

@Component({
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    TableModule,
    InputTextModule,
    IconFieldModule,
    InputIconModule,
    ButtonModule,
    RippleModule
  ],
  templateUrl: './scheduled-jobs.html',
  styleUrl: './scheduled-jobs.css'
})
export default class ScheduledJobsComponent implements OnInit {

  private http = inject(HttpClient);

  /* ---------- Signals ---------- */
  users = signal<AlphaUser[]>([]);
  loading = signal(false);
  tableColumns = signal<Column[]>([]);

  constructor() {}

  ngOnInit(): void {
    this.generateColumns();
    this.loadUsers();
  }

  /* ---------- API ---------- */
  loadUsers(): void {
    this.loading.set(true);
    this.http.get<AlphaUser[]>('/api/alpha-users').subscribe({
      next: data => {
        this.users.set(data);
        this.loading.set(false);
      },
      error: err => {
        console.error('Failed to fetch users:', err);
        this.loading.set(false);
      }
    });
  }

  refresh(): void {
    this.loadUsers();
  }

  /* ---------- Helpers ---------- */
  generateColumns(): void {
    // This is a placeholder. In a real app, you might fetch this from a service
    // or have a more dynamic way of determining columns.
    const userKeys: Array<keyof AlphaUser> = [
      'id', 'rev', 'custom_regcompanyname', 'frunindexedstring1', 'frunindexedstring2', 'frunindexedstring3', 'frunindexedstring4', 'frunindexedstring5',
      'frindexedstring11', 'frindexedstring12', 'frindexedstring10', 'frindexedstring19', 'frindexedstring17', 'frindexedstring18', 'frindexedstring15',
      'frindexedstring16', 'frindexedstring13', 'frindexedstring14', 'givenname', 'frindexedstring20', 'telephonenumber', 'city', 'displayname',
      'accountstatus', 'sn', 'frunindexeddate1', 'frindexedstring9', 'frindexedstring8', 'frindexedstring7', 'frindexedstring6', 'passwordlastchangedtime',
      'country', 'mail', 'frindexeddate5', 'frindexeddate4', 'frindexeddate3', 'frindexedstring5', 'frindexedstring4', 'frindexedstring3', 'frindexedstring2',
      'frindexedstring1', 'frunindexedinteger3', 'frunindexedinteger2', 'frunindexedinteger1', 'description', 'frindexedinteger4', 'frindexedinteger3',
      'frindexedinteger2', 'frindexedinteger1', 'frindexedinteger5', 'username', 'frindexeddate2', 'frindexeddate1'
    ];

    const columns = userKeys.map(key => ({
      field: key,
      header: this.formatHeader(key),
    }));
    this.tableColumns.set(columns);
  }

  formatHeader(field: string): string {
    // Basic formatter: separate camelCase and capitalize
    const result = field.replace(/([A-Z])/g, ' $1');
    return result.charAt(0).toUpperCase() + result.slice(1);
  }
}