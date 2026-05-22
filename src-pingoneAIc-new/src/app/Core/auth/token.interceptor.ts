import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';
import { environment } from '../../../environments/environment';


export const tokenInterceptor: HttpInterceptorFn = (req, next) => {
	const auth = inject(AuthService);
	const token = auth.getAccessToken();
	const isRelativeRequest = req.url.startsWith('/');
	const isConfiguredAbsoluteApiRequest =
		!!environment.pingAicBaseUrl && req.url.startsWith(environment.pingAicBaseUrl);

	if (!token || (!isRelativeRequest && !isConfiguredAbsoluteApiRequest)) {
		return next(req);
	}

	return next(
		req.clone({
			setHeaders: { Authorization: `Bearer ${token}` }
		})
	);
};