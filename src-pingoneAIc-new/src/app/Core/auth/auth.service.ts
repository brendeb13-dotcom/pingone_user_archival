import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { AuthConfig, OAuthService } from 'angular-oauth2-oidc';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly returnUrlKey = 'auth_return_url';
  private readonly oidcConfig: AuthConfig = {
    issuer: environment.oidc.issuer,
    clientId: environment.oidc.clientId,
    scope: environment.oidc.scope,
    responseType: environment.oidc.responseType,
    redirectUri: environment.oidc.redirectUri,
    postLogoutRedirectUri: environment.oidc.postLogoutRedirectUri,
    loginUrl: environment.oidc.loginUrl,
    tokenEndpoint: environment.oidc.tokenEndpoint,
    userinfoEndpoint: environment.oidc.userinfoEndpoint,
    logoutUrl: environment.oidc.logoutUrl,
    requireHttps: environment.oidc.requireHttps,
    strictDiscoveryDocumentValidation: environment.oidc.strictDiscoveryDocumentValidation,
    showDebugInformation: !environment.production,
    oidc: true,
  };

  constructor(
    private router: Router,
    private oauthService: OAuthService,
  ) {
    this.oauthService.configure(this.oidcConfig);
    this.oauthService.setStorage(localStorage);
    this.oauthService.setupAutomaticSilentRefresh();
  }

  async login(targetUrl = '/dashboard'): Promise<void> {
    sessionStorage.setItem(this.returnUrlKey, targetUrl);
    this.oauthService.initCodeFlow();
  }

  async completeLogin(): Promise<boolean> {
    await this.oauthService.tryLoginCodeFlow();

    if (!this.isAuthenticated()) {
      return false;
    }

    const targetUrl = sessionStorage.getItem(this.returnUrlKey) || '/dashboard';
    sessionStorage.removeItem(this.returnUrlKey);
    await this.router.navigateByUrl(targetUrl);
    return true;
  }

  logout(): void {
    sessionStorage.removeItem(this.returnUrlKey);
    this.oauthService.logOut();
  }

  isAuthenticated(): boolean {
    return this.oauthService.hasValidAccessToken();
  }

  getAccessToken(): string {
    return this.oauthService.getAccessToken();
  }
}
