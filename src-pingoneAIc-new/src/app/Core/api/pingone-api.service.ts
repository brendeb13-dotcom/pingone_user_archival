import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';


@Injectable({ providedIn: 'root' })
export class PingoneApiService {
    private baseUrl = environment.pingAicBaseUrl;
    private apiVersion = 'protocol=2.1,resource=1.0';

    constructor(private http: HttpClient) { }

    getRequestOptions(params: {}, customerHeaders = {}) {
    const headers = new HttpHeaders(
      Object.assign(
        {},
        {
                    'Accept-API-Version': this.apiVersion,
        },
        customerHeaders
      )
    );
    return { params, headers };
  }

    /**
       * Get Job History for a specific scheduled job
       * Example: Daily_Onboarding
       */
    getAlphaUser() {
        const headers = new HttpHeaders({
            'Accept-API-Version': this.apiVersion,
        });

        const params = new HttpParams()
            .set('_queryFilter', `frIndexedString3 eq "deactivated"`)
            .set('_pageSize', '50');

        const base = this.baseUrl || '';
        return this.http.get(`${base}/openidm/managed/alpha_user`,{ headers, params }
        );
    }


    offboarding(opts: { filter?: string; page?: number; size?: number; search?: string; sort?: string; }) {
        const headers = new HttpHeaders({
            'Accept-API-Version': this.apiVersion,
        });
        let params = new HttpParams();
        if (opts?.filter) {
            // Translate simple filter to IDM _queryFilter; adjust as needed
            params = params.set('_queryFilter', opts.filter.replace('lifecycleStatus', 'frIndexedString3'));
        } else {
            params = params.set('_queryFilter', 'true');
        }
        if (opts?.size != null) params = params.set('_pageSize', String(opts.size));
        if (opts?.page != null) params = params.set('_pagedResultsOffset', String((opts.page || 0) * (opts.size || 10)));
        if (opts?.sort) params = params.set('_sortKeys', opts.sort);
        if (opts?.search) params = params.set('_queryFilter', `(username co "${opts.search}")`);

        const base = this.baseUrl || '';
        return this.http.get(`${base}/openidm/managed/users`, { headers, params });
    }


    scheduledJobs(params: any) {
        const headers = new HttpHeaders({
            'Accept-API-Version': this.apiVersion
        });

        const base = this.baseUrl || '';
        return this.http.get(
            `${base}/openidm/scheduler/job`,
            { headers, params }
        );
    }


    failedJobs(params: any) {
        const base = this.baseUrl || '';
        return this.http.get(`${base}/jobs/failed`, { params });
    }


    emailTemplates() {
        const base = this.baseUrl || '';
        return this.http.get(`${base}/email/templates`);
    }
}
