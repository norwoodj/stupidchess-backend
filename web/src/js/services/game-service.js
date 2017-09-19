export default class GameService {
    constructor(http) {
        this.http = http;
    }

    createGame(createRequest) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: "POST",
                url: "/api/game/",
                data: JSON.stringify(createRequest),
                contentType: "application/json",
                success: game => resolve(game),
                error: error => reject(error)
            });
        });
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

    getActiveGames(gameType) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/active${gameType != null ? `?gameType=${gameType}` : ""}`,
                success: game => resolve(game),
                error: (error) => reject(error)
            })
        });
    }

    getCompletedGames(userUuid, gameType) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/completed?userUuid=${userUuid}${gameType != null ? `&gameType=${gameType}` : ""}`,
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