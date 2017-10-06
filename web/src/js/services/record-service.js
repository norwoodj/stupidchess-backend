
export default class RecordService {
    constructor(http, errorHandler) {
        this.http = http;
        this.errorHandler = errorHandler;
    }

    getUserGameRecords(userUuid, gameType) {
        return new Promise(resolve => {
            this.http.ajax({
                type: "GET",
                url: `/api/record/?userUuid=${userUuid}${gameType != null ? `&gameType=${gameType}` : ""}`,
                success: user_records => resolve(user_records),
                error: this.errorHandler
            });
        });
    }
}
