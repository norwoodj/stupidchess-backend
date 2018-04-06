
export default class RecordService {
    constructor(http, errorHandler) {
        this.http = http;
        this.errorHandler = errorHandler;
    }

    getUserGameRecords(userUuid, gameType, includeOnePlayerGames) {
        return new Promise(resolve => {
            this.http.ajax({
                type: "GET",
                url: `/api/record/?userUuid=${userUuid}&includeOnePlayerGames=${includeOnePlayerGames}${gameType != null ? `&gameType=${gameType}` : ""}`,
                success: user_records => resolve(user_records),
                error: this.errorHandler
            });
        });
    }
}
