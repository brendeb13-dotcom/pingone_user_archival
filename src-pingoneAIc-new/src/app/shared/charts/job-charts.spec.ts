import { ComponentFixture, TestBed } from '@angular/core/testing';

import JobChartsComponent from './job-charts.component';

describe('JobCharts', () => {
  let component: JobChartsComponent;
  let fixture: ComponentFixture<JobChartsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JobChartsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(JobChartsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
