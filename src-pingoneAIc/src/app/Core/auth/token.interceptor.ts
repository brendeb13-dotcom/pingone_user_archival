import { HttpInterceptorFn } from '@angular/common/http';

export const tokenInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('TOKEN_KEY');
  return next(req.clone({
    setHeaders: token ? { Authorization: `Bearer ${token}` } : {}
  }));
};