import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class FlaskBackendService {

    constructor(private http: HttpClient) {}

    async authenticate(username: string, password: string) : Promise<any> {
        const response = await this.http.post<any>('/users/authenticate', {username, password}).toPromise();
        return response;
    }

    async register(username: string, password: string) : Promise<any> {
        const response = await this.http.post<any>('/users/register', {username, password}).toPromise();
        return response;
    }

    async updateUser(id: string, params: any) : Promise<any> {
        const response = await this.http.put<any>(`/users/${id}`, params).toPromise();
        return response;
    }

    async deleteUser(id: string) : Promise<any> {
        const response = await this.http.delete<any>(`/users/${id}`).toPromise();
        return response;
    }
}
