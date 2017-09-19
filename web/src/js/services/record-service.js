export default class RecordService {
    constructor(http) {
        this.http = http;
    }

    getUserGameRecords(userUuid, gameType) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: "GET",
                url: `/api/record/?userUuid=${userUuid}${gameType != null ? `&gameType=${gameType}` : ""}`,
                success: user_records => resolve(user_records),
                error: error => reject(error)
            });
        });
    }
}