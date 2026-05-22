import { ComponentFixture, TestBed } from '@angular/core/testing';

import FailedJobsComponent from './failed-jobs.component';

describe('FailedJobs', () => {
  let component: FailedJobsComponent;
  let fixture: ComponentFixture<FailedJobsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FailedJobsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FailedJobsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
