import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-email-templates',
  imports: [CommonModule],
  templateUrl: './email-templates.html',
  styleUrl: './email-templates.css'
})
export class EmailTemplates {
  // Template variables for display
  firstName = 'firstName';
  lastName = 'lastName';
  email = 'email';
  company = 'company';
  joinDate = 'joinDate';
}
