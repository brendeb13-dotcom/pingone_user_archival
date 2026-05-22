import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-pagination',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './pagination.component.html'
})
export class PaginationComponent {
@Input() total = 0;
@Input() size = 10;
@Output() pageChange = new EventEmitter<number>();


get pages() {
return Array(Math.ceil(this.total / this.size)).fill(0);
}
}