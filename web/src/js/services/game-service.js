export default class GameService {
    constructor(http) {
        this.http = http;
    }

    getGames() {
        return [];
    }

    getGameByUuid(gameUuid) {
        console.log(gameUuid);

        return new Promise((resolve) => {
            resolve({
                gameType: 'STUPID_CHESS',
                lastMove: 2,
                placePieceRequired: true,
                pieces: [
                    {type: 'KING', color: 'BLACK', square: 1},
                    {type: 'QUEEN', color: 'WHITE', square: 116}
                ],
                captures: [],
                currentTurn: null,
                blackUsername: 'John',
                blackScore: 2,
                whiteUsername: 'Erin',
                whiteScore: 1,
                piecesToBePlaced: [
                    {type: 'KING', color: 'BLACK', square: 1},
                    {type: 'QUEEN', color: 'WHITE', square: 116}
                ],
                possiblePlacements: [
                    1,2,3,4
                ]
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
        console.log(gameUuid);
        console.log('Making move');
        console.log(move);
        return new Promise((resolve) => resolve('yay'));
    }
}