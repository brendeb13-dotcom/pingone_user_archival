import { Component } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';


@Component({
  selector: 'app-job-charts',
  standalone: true,
  imports: [BaseChartDirective],
  templateUrl: './job-charts.component.html'
})
export class JobChartsComponent {
data = {
labels: ['Success', 'Failed', 'Running'],
datasets: [{ data: [10, 3, 2] }]
};
}