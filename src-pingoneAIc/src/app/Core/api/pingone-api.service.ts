import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { map, Observable } from 'rxjs';
import { AlphaUser, OpenIdmResponse } from '../../Core/models/user.model';

// Define the new data models to match the backend
interface DashboardUser {
  name: string | null;
  email: string | null;
  country: string | null;
  accountstatus: string | null;
  operation_type: string | null;
}

interface DashboardCard {
  count: number;
  users: DashboardUser[];
}

interface DashboardData {
  employee: DashboardCard;
  contractor: DashboardCard;
  other: DashboardCard;
  total_users: number;
  active_users: number;
  inactive_users: number;
  other_status_users: number;
  add_ops: number;
  update_ops: number;
  today_count: number;
  week_count: number;
  month_count: number;
}

@Injectable({ providedIn: 'root' })
export class PingoneApiService {
    private backendUrl = environment.backendApiUrl;

    constructor(private http: HttpClient) { }

    getDashboardData(): Observable<DashboardData> {
        return this.http.get<DashboardData>(
            `${this.backendUrl}/api/dashboard-data`
        );
    }

    getTimelyUsers(period: string): Observable<DashboardUser[]> {
        return this.http.get<DashboardUser[]>(
            `${this.backendUrl}/api/users/timely`,
            { params: { period } }
        );
    }

    getAlphaUser(): Observable<OpenIdmResponse<AlphaUser>> {
        return this.http.get<OpenIdmResponse<AlphaUser>>(
            `${this.backendUrl}/api/alpha-users`
        );
    }

    getArchivedAlphaUsers(): Observable<OpenIdmResponse<AlphaUser>> {
        return this.http.get<OpenIdmResponse<AlphaUser>>(
            `${this.backendUrl}/api/deleted-users`
        );
    }

    getJobs(): Observable<any> {
        return this.http.get<any>(
            `${this.backendUrl}/api/jobs`
        );
    }

    searchUsers(queryFilter: string) {
        return this.http
            .get<any>(`${this.backendUrl}/api/alpha-users/search`, {
                params: { filter: queryFilter, pageSize: '500' }
            })
            .pipe(map((res: any) => res.result || []));
    }

    getDashboardUsers() {
        return this.http.get<any>(
            `${this.backendUrl}/api/users/dashboard`
        );
    }

    insertAlphaUsers(users: AlphaUser[]) {
        return this.http.post(
            `${this.backendUrl}/api/alpha-users/insert`,
            users
        );
    }

    archiveDeletedUsers(users: AlphaUser[]) {
        return this.http.post(
            `${this.backendUrl}/api/alpha-users/archive`,
            users
        );
    }

    getDeletedUsersStream(): Observable<AlphaUser[]> {
        return this.http.get<AlphaUser[]>(
            `${this.backendUrl}/api/deleted-users/stream`
        );
    }
}