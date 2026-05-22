import { Component } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-job-charts',
  standalone: true,
  imports: [BaseChartDirective],
  template: `
    <div class="chart-container">
      <canvas
        baseChart
        [data]="pieChartData"
        [type]="'pie'"
        [options]="pieChartOptions"
      >
      </canvas>
    </div>
  `,
  styles: [`
    .chart-container {
      position: relative;
      height: 40vh;
      width: 80vw;
    }
  `]
})
export class JobChartsComponent {
  // Mock data for the chart
  public pieChartData = {
    labels: ['Success', 'Failure', 'In Progress'],
    datasets: [
      {
        data: [300, 50, 100],
        backgroundColor: ['#4CAF50', '#F44336', '#FFC107'],
      },
    ],
  };

  public pieChartOptions = {
    responsive: true,
  };
}