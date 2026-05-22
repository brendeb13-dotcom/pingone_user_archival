import { Component } from '@angular/core';
import { JobChartsComponent } from '../../shared/charts/job-charts.component';

@Component({
  standalone: true,
  imports: [JobChartsComponent],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export default class DashboardComponent {}
