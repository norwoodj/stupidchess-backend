export default class RecordService {
    constructor(http) {
        this.http = http;
    }

    getUserGameRecords(user_id) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: "GET",
                url: `/api/record/?userUuid=${user_id}`,
                success: user_records => resolve(user_records),
                error: error => reject(error)
            });
        });
    }
}