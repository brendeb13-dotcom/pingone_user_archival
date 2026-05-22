import { ComponentFixture, TestBed } from '@angular/core/testing';

import ScheduledJobsComponent from './scheduled-jobs.component';

describe('ScheduledJobs', () => {
  let component: ScheduledJobsComponent;
  let fixture: ComponentFixture<ScheduledJobsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ScheduledJobsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ScheduledJobsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
