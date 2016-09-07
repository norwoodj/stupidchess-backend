export default class GameService {
    constructor(http) {
        this.http = http;
    }

    getGames() {
        return [];
    }

    getGameByUuid(gameUuid) {
        return new Promise((resolve, reject) => {
            this.http.ajax({
                type: 'GET',
                url: `/api/game/${gameUuid}`,
                success: game => resolve(game),
                error: (error) => reject(error)
            });
        });
    }

    getPossibleMoves(gameUuid, square) {
        console.log(gameUuid);
        return new Promise((resolve) => {
            resolve([
                {move: square - 10, captures: []},
                {move: square - 20, captures: []},
                {move: square - 30, captures: []},
                {move: square - 40, captures: []},
                {move: square - 50, captures: [square - 50]},
                {move: square + 10, captures: []},
                {move: square - 1, captures: []},
                {move: square - 2, captures: []},
                {move: square + 1, captures: []},
                {move: square + 2, captures: []}
            ]);
        });
    }

    makeMove(gameUuid, move) {
        return new Promise(
            (resolve, reject) => {
                this.http.post(
                    `/api/game/${gameUuid}/move/`,
                    JSON.stringify(move),
                    (response) => resolve(response),
                    'json',
                ).fail((error) => reject(error));
            }
        );
    }
}