import { Routes } from '@angular/router';
import { authGuard } from './Core/auth/auth.guard';
import { AppLayoutComponent } from './layout/app-layout.component';

export const routes: Routes = [

  // 🔓 Public
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.component').then(m => m.default)
  },
  {
    path: 'auth/callback',
    loadComponent: () => import('./pages/login/auth-callback.component').then(m => m.AuthCallbackComponent)
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
        path: 'offboarding',
        loadComponent: () => import('./pages/offboarding/offboarding.component').then(m => m.default)
      },
      {
        path: 'scheduled-jobs',
        loadComponent: () => import('./pages/scheduled-jobs/scheduled-jobs.component').then(m => m.default)
      },
      {
        path: 'failed-jobs',
        loadComponent: () => import('./pages/failed-jobs/failed-jobs.component').then(m => m.default)
      },
      {
        path: 'email-templates',
        loadComponent: () => import('./pages/email-templates/email-templates.component').then(m => m.EmailTemplates)
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
