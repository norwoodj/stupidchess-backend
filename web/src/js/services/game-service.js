export default class GameService {
    constructor(http) {
        this.http = http;
    }

    getPossibleMoves(gameUuid, square) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/${gameUuid}/move/possible?square=${square}`,
                success: possibleMoves => resolve(possibleMoves),
                error: error => reject(error)
            });
        });
    }

    static getGameListQueryString(userUuid, gameType) {
        return `?userUuid=${userUuid}${gameType != null ? `&gameType=${gameType}` : ""}`
    }

    getActiveGames(userUuid, gameType) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/active${GameService.getGameListQueryString(userUuid, gameType)}`,
                success: game => resolve(game),
                error: (error) => reject(error)
            })
        });
    }

    getCompletedGames(userUuid, gameType) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/completed${GameService.getGameListQueryString(userUuid, gameType)}`,
                success: game => resolve(game),
                error: (error) => reject(error)
            })
        });
    }

    getGameByUuid(gameUuid) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/${gameUuid}`,
                success: game => resolve(game),
                error: (error) => reject(error)
            });
        });
    }

    makeMove(gameUuid, move) {
        return new Promise(
            (resolve, reject) => {
                this.http.ajax({
                    type: "POST",
                    url: `/api/game/${gameUuid}/move/`,
                    data: JSON.stringify(move),
                    contentType: "application/json",
                    success: (response) => resolve(response),
                    error: (error) => reject(error)
                });
            }
        );
    }
}