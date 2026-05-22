import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../Core/auth/auth.service';

@Component({
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export default class LoginComponent {
  username = '';
  password = '';
  error = false;
  errorMessage = '';
  isLoading = false;

  constructor(private auth: AuthService, private router: Router) {}

  async login() {
    this.error = false;
    this.errorMessage = '';
    this.isLoading = true;

    try {
      const success = await this.auth.login(this.username, this.password);
      if (success) {
        this.router.navigate(['/dashboard']);
      } else {
        this.error = true;
        this.errorMessage = 'Invalid username or password';
      }
    } catch (err: any) {
      this.error = true;
      this.errorMessage = err?.error?.message || 'Login failed. Please try again.';
    } finally {
      this.isLoading = false;
    }
  }
}
