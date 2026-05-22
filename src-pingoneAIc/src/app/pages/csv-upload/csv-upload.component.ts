import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

interface UploadResponse {
  message: string;
  inserted: number;
  updated: number;
  failed: number;
  failed_rows: any[];
}

@Component({
  selector: 'app-csv-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './csv-upload.component.html',
  styleUrl: './csv-upload.component.css'
})
export class CsvUploadComponent {
  private http = inject(HttpClient);

  constructor() {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) {
      return;
    }
    const file = input.files[0];
    const formData = new FormData();
    formData.append('file', file, file.name);

    this.http.post<UploadResponse>('/api/alpha-users/upload-csv', formData).subscribe({
      next: (response) => {
        console.log('Upload successful', response);
        alert(`Upload successful! Inserted: ${response.inserted}, Updated: ${response.updated}`);
      },
      error: (err) => {
        console.error('Upload failed', err);
        alert(`Upload failed: ${err.error?.detail || 'An unknown error occurred'}`);
      }
    });
  }
}