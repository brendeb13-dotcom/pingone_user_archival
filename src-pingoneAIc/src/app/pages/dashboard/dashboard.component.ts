import {
  Component,
  OnInit,
  AfterViewInit,
  ViewChild,
  ElementRef,
  signal,
  inject
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { Chart, registerables } from 'chart.js';
import { PingoneApiService } from '../../Core/api/pingone-api.service';

interface DashboardUser {
  name: string | null;
  email: string | null;
  country: string | null;
  accountstatus: string | null;
  operation_type: string | null;
}

interface DashboardCard {
  count: number;
  users: DashboardUser[];
}

interface DashboardData {
  employee: DashboardCard;
  contractor: DashboardCard;
  other: DashboardCard;
  total_users: number;
  active_users: number;
  inactive_users: number;
  other_status_users: number;
  add_ops: number;
  update_ops: number;
  today_count: number;
  week_count: number;
  month_count: number;
}

Chart.register(...registerables);

@Component({
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export default class DashboardComponent
  implements OnInit, AfterViewInit {

  @ViewChild('statusChart')
  statusChartRef!: ElementRef<HTMLCanvasElement>;

  @ViewChild('operationChart')
  operationChartRef!: ElementRef<HTMLCanvasElement>;

  @ViewChild('trendChart')
  trendChartRef!: ElementRef<HTMLCanvasElement>;

  private statusChartInstance?: Chart;
  private operationChartInstance?: Chart;
  private trendChartInstance?: Chart;

  private api = inject(PingoneApiService);

  dashboardData = signal<DashboardData | null>(null);

  employeeCard = signal<DashboardCard>({
    count: 0,
    users: []
  });

  contractorCard = signal<DashboardCard>({
    count: 0,
    users: []
  });

  otherCard = signal<DashboardCard>({
    count: 0,
    users: []
  });

  totalUsers = signal(0);
  activeUsers = signal(0);
  inactiveUsers = signal(0);
  otherStatusUsers = signal(0);

  addOps = signal(0);
  updateOps = signal(0);

  todayCount = signal(0);
  weekCount = signal(0);
  monthCount = signal(0);

  gridTitle = signal('Employees');
  gridData = signal<DashboardUser[]>([]);
  loading = signal(true);

  ngOnInit(): void {
    this.loadDashboardData();
  }

  ngAfterViewInit(): void {
  }

  loadDashboardData(): void {

    this.loading.set(true);

    this.api.getDashboardData().subscribe({

      next: (data) => {

        this.dashboardData.set(data);

        this.employeeCard.set(data.employee);
        this.contractorCard.set(data.contractor);
        this.otherCard.set(data.other);

        this.totalUsers.set(data.total_users);
        this.activeUsers.set(data.active_users);
        this.inactiveUsers.set(data.inactive_users);
        this.otherStatusUsers.set(data.other_status_users);

        this.addOps.set(data.add_ops);
        this.updateOps.set(data.update_ops);

        this.todayCount.set(data.today_count);
        this.weekCount.set(data.week_count);
        this.monthCount.set(data.month_count);

        this.gridData.set(data.employee.users);
        this.gridTitle.set('Employees');

        this.loading.set(false);

        this.renderCharts();
      },

      error: (err) => {

        console.error(
          'Failed to load dashboard data:',
          err
        );

        this.loading.set(false);
      }
    });
  }

  showUserType(
    type: 'employee' | 'contractor' | 'other'
  ): void {

    const data = this.dashboardData();

    if (!data) return;

    if (type === 'employee') {

      this.gridTitle.set('Employees');
      this.gridData.set(data.employee.users);

    } else if (type === 'contractor') {

      this.gridTitle.set('Contractors');
      this.gridData.set(data.contractor.users);

    } else {

      this.gridTitle.set('Others');
      this.gridData.set(data.other.users);
    }
  }

  showTimelyUsers(
    period: 'today' | 'week' | 'month'
  ): void {

    this.loading.set(true);

    let title = '';

    if (period === 'today') {

      title = "Today's Updates";

    } else if (period === 'week') {

      title = "This Week's Updates";

    } else {

      title = "This Month's Updates";
    }

    this.gridTitle.set(title);

    this.api.getTimelyUsers(period).subscribe({

      next: (users) => {

        this.gridData.set(users);
        this.loading.set(false);
      },

      error: (err) => {

        console.error(
          `Failed to load users for period: ${period}`,
          err
        );

        this.gridData.set([]);
        this.loading.set(false);
      }
    });
  }

  renderCharts(): void {

    if (
      !this.statusChartRef ||
      !this.operationChartRef ||
      !this.trendChartRef
    ) {

      console.error(
        'Chart canvas elements not found!'
      );

      return;
    }

    this.statusChartInstance?.destroy();
    this.operationChartInstance?.destroy();
    this.trendChartInstance?.destroy();

    // User Distribution Chart

    this.statusChartInstance = new Chart(
      this.statusChartRef.nativeElement,
      {
        type: 'doughnut',

        data: {
          labels: [
            'Active',
            'Inactive',
            'Others'
          ],

          datasets: [{
            data: [
              this.activeUsers(),
              this.inactiveUsers(),
              this.otherStatusUsers()
            ],

            backgroundColor: [
              '#22c55e',
              '#facc15',
              '#ef4444'
            ],

            borderWidth: 1
          }]
        },

        options: {
          responsive: true,
          maintainAspectRatio: false,

          plugins: {
            legend: {
              position: 'bottom'
            }
          }
        }
      }
    );

    // Add / Update Doughnut Chart

    this.operationChartInstance = new Chart(
      this.operationChartRef.nativeElement,
      {
        type: 'doughnut',

        data: {
          labels: [
            'Add',
            'Update'
          ],

          datasets: [{
            data: [
              this.addOps(),
              this.updateOps()
            ],

            backgroundColor: [
              '#3b82f6',
              '#14b8a6'
            ],

            borderWidth: 1
          }]
        },

        options: {
          responsive: true,
          maintainAspectRatio: false,

          plugins: {
            legend: {
              position: 'bottom'
            }
          }
        }
      }
    );

    // Trend Chart

    // Trend Chart

this.trendChartInstance = new Chart(
  this.trendChartRef.nativeElement,
  {
    type: 'bar',

    data: {
      labels: [
        'ADD Ops',
        'UPDATE Ops'
      ],

      datasets: [{
        label: 'Operations',

        data: [
          this.addOps(),
          this.updateOps()
        ],

        backgroundColor: [
          '#3b82f6',
          '#14b8a6'
        ],

        borderRadius: 8,
        borderWidth: 1
      }]
    },

    options: {
      responsive: true,
      maintainAspectRatio: false,

      plugins: {
        legend: {
          display: false
        }
      },

      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  }
);
  }
}