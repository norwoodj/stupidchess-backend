
export default class GameService {
    constructor(http, errorHandler) {
        this.http = http;
        this.errorHandler = errorHandler;
    }

    static getMoveListQueryString(offset, limit) {
        return `?offset=${offset}&limit=${limit}`;
    }

    static getGameListQueryString(userUuid, gameType, offset, limit) {
        return `?userUuid=${userUuid}&offset=${offset}&limit=${limit}${gameType != null ? `&gameType=${gameType}` : ""}`;
    }

    static getGameCountQueryString(userUuid, gameType) {
        return `?userUuid=${userUuid}${gameType != null ? `&gameType=${gameType}` : ""}`;
    }

    getActiveGames(userUuid, gameType, offset, limit) {
        return new Promise(resolve => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/active${GameService.getGameListQueryString(userUuid, gameType, offset, limit)}`,
                success: game => resolve(game),
                error: this.errorHandler
            });
        });
    }

    getCompletedGames(userUuid, gameType, offset, limit) {
        return new Promise(resolve => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/completed${GameService.getGameListQueryString(userUuid, gameType, offset, limit)}`,
                success: game => resolve(game),
                error: this.errorHandler
            });
        });
    }

    getActiveGameCount(userUuid, gameType) {
        return new Promise(resolve => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/active/count${GameService.getGameCountQueryString(userUuid, gameType)}`,
                success: res => resolve(res.gameCount),
                error: this.errorHandler
            });
        });
    }

    getCompletedGameCount(userUuid, gameType) {
        return new Promise(resolve => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/completed/count${GameService.getGameCountQueryString(userUuid, gameType)}`,
                success: res => resolve(res.gameCount),
                error: this.errorHandler
            });
        });
    }

    getGameByUuid(gameUuid) {
        return new Promise(resolve => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/${gameUuid}`,
                success: game => resolve(game),
                error: this.errorHandler
            });
        });
    }

    getPossibleMoves(gameUuid, square) {
        return new Promise(resolve => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/${gameUuid}/possible-move?square=${square}`,
                success: possibleMoves => resolve(possibleMoves),
                error: this.errorHandler
            });
        });
    }

    getMovesForGame(gameUuid, offset, limit) {
        return new Promise(resolve => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/${gameUuid}/move${GameService.getMoveListQueryString(offset, limit)}`,
                success: (response) => resolve(response),
                error: this.errorHandler
            });
        });
    }

    getMoveCountForGame(gameUuid) {
        return new Promise(resolve => {
            this.http.ajax({
                type: "GET",
                url: `/api/game/${gameUuid}/move/count`,
                success: (response) => resolve(response.moveCount),
                error: this.errorHandler
            });
        });
    }

    makeMove(gameUuid, move) {
        return new Promise(resolve => {
            this.http.ajax({
                type: "POST",
                url: `/api/game/${gameUuid}/move`,
                data: JSON.stringify(move),
                contentType: "application/json",
                success: (response) => resolve(response),
                error: this.errorHandler
            });
        });
    }
}
