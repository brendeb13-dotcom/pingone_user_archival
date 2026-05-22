import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../Core/auth/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './header.html',
  styleUrl: './header.css'
})
export class HeaderComponent {
  lastLogin: string | null = null;
  username: string | null = null;

  constructor(private auth: AuthService) {
    this.lastLogin = this.auth.getLastLogin();
    this.username = this.auth.getUsername();
  }
  
  logout() {
    this.auth.logout();
  }
}