import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  imports: [RouterModule, CommonModule],
  selector: 'app-sidebar',
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css'
})
export class SidebarComponent {
  menuItems = [
    { icon: '📊', label: 'Dashboard', route: '/dashboard' },
    { icon: '👥', label: 'Offboarding Users', route: '/offboarding' },
    { icon: '⏰', label: 'Scheduled Jobs', route: '/scheduled-jobs' },
    { icon: '⚠️', label: 'Failed Jobs', route: '/failed-jobs' },
    { icon: '📧', label: 'Email Templates', route: '/email-templates' }
  ];

  isCollapsed = false;

  toggleCollapse() {
    this.isCollapsed = !this.isCollapsed;
  }
}
