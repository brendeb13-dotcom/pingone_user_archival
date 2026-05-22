import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './auth.service';

export const authGuard = async (_route: unknown, state: { url: string }) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (auth.isAuthenticated()) {
    return true;
  }

  await auth.login(state.url || '/dashboard');
  return router.createUrlTree(['/login']);
};
