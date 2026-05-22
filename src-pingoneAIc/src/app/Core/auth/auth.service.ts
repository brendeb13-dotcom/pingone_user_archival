import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { jwtDecode } from 'jwt-decode';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private TOKEN_KEY = 'TOKEN_KEY';
  private LAST_LOGIN_KEY = 'LAST_LOGIN_KEY';
  private USERNAME_KEY = 'USERNAME_KEY';

  constructor(private router: Router, private http: HttpClient) {}

  login(username: string, password: string) {
    return this.http.post<{ access_token: string, token_type: string }>(
      `${environment.backendApiUrl}/api/auth/login`,
      { username, password }
    ).toPromise().then((response: any) => {
      if (response?.access_token) {
        const decodedToken: any = jwtDecode(response.access_token);
        localStorage.setItem(this.TOKEN_KEY, response.access_token);
        localStorage.setItem(this.LAST_LOGIN_KEY, decodedToken.last_login);
        localStorage.setItem(this.USERNAME_KEY, decodedToken.sub); // 'sub' is the standard JWT claim for username
        return true;
      }
      return false;
    }).catch((error: any) => {
      console.error('Login failed:', error);
      return false;
    });
  }

  logout() {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.LAST_LOGIN_KEY);
    localStorage.removeItem(this.USERNAME_KEY);
    this.router.navigate(['/login']);
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem(this.TOKEN_KEY);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  getLastLogin(): string | null {
    return localStorage.getItem(this.LAST_LOGIN_KEY);
  }

  getUsername(): string | null {
    return localStorage.getItem(this.USERNAME_KEY);
  }
}