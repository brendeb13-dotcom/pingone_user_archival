import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';


@Injectable({ providedIn: 'root' })
export class RealtimeService {
connect() {
return new EventSource(`${environment.pingAicBaseUrl}/jobs/status/stream`);
}
}