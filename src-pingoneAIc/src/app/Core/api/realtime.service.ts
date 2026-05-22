import { Injectable } from '@angular/core';
import { interval, switchMap } from 'rxjs';
import { PingoneApiService } from './pingone-api.service';
import { AlphaUser } from '../models/user.model';

@Injectable({ providedIn: 'root' })
export class RealtimeService {
  private pollingInterval = 30000; // 30 seconds

  constructor(private api: PingoneApiService) {}

  startPollingDeletedUsers() {
    return interval(this.pollingInterval).pipe(
      switchMap(() => this.api.getDeletedUsersStream())
    );
  }

  // For backward compatibility
  connect() {
    return new EventSource('/api/deleted-users/stream');
  }
}