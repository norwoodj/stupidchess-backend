export default class UserService {
    constructor(http) {
        this.http = http;
    }

    getCurrentUser() {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: 'GET',
                url: '/api/user/',
                contentType: 'application/json',
                success: response => resolve(response),
                error: (error) => reject(error)
            });
        });
    }

    login(username, password) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: 'POST',
                url: '/api/user/login',
                data: JSON.stringify({username: username, password: password}),
                contentType: 'application/json',
                success: response => resolve(response),
                error: (error) => reject(error)
            });
        });
    }

    createUser(username, password) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: 'POST',
                url: '/api/user/',
                data: JSON.stringify({username: username, password: password}),
                contentType: 'application/json',
                success: response => resolve(response),
                error: (error) => reject(error)
            });
        });
    }
}
