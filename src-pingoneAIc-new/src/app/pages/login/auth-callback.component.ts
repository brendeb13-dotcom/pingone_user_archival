import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../Core/auth/auth.service';

@Component({
  selector: 'app-auth-callback',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="login-container">
      <div class="login-wrapper">
        <div class="login-card">
          <div class="login-header">
            <h1>Signing You In</h1>
            <p>Completing the PingOne AIC callback.</p>
          </div>

          <div *ngIf="error" class="error-message">
            {{ error }}
          </div>
        </div>
      </div>
    </div>
  `,
})
export class AuthCallbackComponent {
  error = '';

  constructor(
    private auth: AuthService,
    private route: ActivatedRoute,
    private router: Router,
  ) {
    void this.handleCallback();
  }

  private async handleCallback(): Promise<void> {
    const error = this.route.snapshot.queryParamMap.get('error');
    const errorDescription = this.route.snapshot.queryParamMap.get('error_description');

    if (error) {
      await this.router.navigate(['/login'], {
        queryParams: {
          authError: errorDescription || error,
        },
      });
      return;
    }

    try {
      const isAuthenticated = await this.auth.completeLogin();

      if (!isAuthenticated) {
        this.error = 'Sign-in could not be completed. Check the PingOne AIC client configuration and try again.';
      }
    } catch {
      this.error = 'The authorization response was rejected. Verify the callback URL and token endpoint settings in PingOne AIC.';
      await this.router.navigate(['/login'], {
        queryParams: {
          authError: this.error,
        },
      });
    }
  }
}