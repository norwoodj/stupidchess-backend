export default class UserService {
    constructor(http) {
        this.http = http;
    }

    getUserForUuid(userUuid) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: "GET",
                url: `/api/user/?userUuid=${userUuid}`,
                contentType: "application/json",
                success: response => resolve(response),
                error: (error) => reject(error)
            });
        });
    }

   logout() {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: "POST",
                url: "/logout",
                success: response => resolve(response),
                error: (error) => reject(error)
            });
        });
    }

   changePassword(username, password, newPassword) {
       return new Promise((resolve, reject) => {
           this.http.ajax({
               type: "POST",
               url: "/api/user/change-password",
               data: JSON.stringify({username: username, password: password, newPassword: newPassword}),
               contentType: "application/json",
               success: response => resolve(response),
               error: (error) => reject(error)
           });
       });
   }
}
