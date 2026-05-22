import { Routes } from '@angular/router';
import { authGuard } from './Core/auth/auth.guard';
import { AppLayoutComponent } from './layout/app-layout.component';

export const routes: Routes = [

  // 🔓 Public
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.component').then(m => m.default)
  },

  // 🔐 Protected Layout
  {
    path: '',
    component: AppLayoutComponent,
    canActivate: [authGuard],
    children: [
      {
        path: 'dashboard',
        loadComponent: () => import('./pages/dashboard/dashboard.component').then(m => m.default)
      },
      {
        path: 'all-users',
        loadComponent: () => import('./pages/scheduled-jobs/scheduled-jobs.component').then(m => m.default)
      },
      {
        path: 'csv-upload',
        loadComponent: () => import('./pages/csv-upload/csv-upload.component').then(m => m.CsvUploadComponent)
      },
      {
        path: 'job-logs',
        loadComponent: () => import('./pages/job-logs/job-logs.component').then(m => m.JobLogsComponent)
      },
      {
        path: '',
        redirectTo: '/dashboard',
        pathMatch: 'full'
      }
    ]
  },

  { path: '**', redirectTo: '/login' }
];