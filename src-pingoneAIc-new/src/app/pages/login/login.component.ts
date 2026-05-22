import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from '../../Core/auth/auth.service';

@Component({
  standalone: true,
  imports: [CommonModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export default class LoginComponent {
  error = false;
  errorMessage = 'Complete the PingOne sign-in flow to access the portal.';
  isLoading = false;

  constructor(
    private auth: AuthService,
    private route: ActivatedRoute,
  ) {
    const authError = this.route.snapshot.queryParamMap.get('authError');

    if (authError) {
      this.error = true;
      this.errorMessage = authError;
    }
  }

  async login() {
    this.error = false;
    this.isLoading = true;

    try {
      await this.auth.login('/dashboard');
    } catch {
      this.error = true;
      this.errorMessage = 'Unable to start PingOne sign-in. Verify the OIDC settings in the environment files.';
      this.isLoading = false;
    }
  }
}
