function GameService(http) {
    this.http = http;
}

GameService.prototype = {
    getGames: function () {
        return [];
    },

    getGameByUuid: function (gameUuid) {
        if (!this.second) {
            this.second = true;

            return new Promise((resolve, reject) => {
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
                        {type: 'KING', color: 'BLACK'},
                        {type: 'QUEEN', color: 'WHITE'}
                    ],
                    possiblePlacements: [
                        0, 1, 2, 3
                    ]
                });
            });
        }
        return new Promise((resolve, reject) => {
            resolve({
                gameType: 'STUPID_CHESS',
                lastMove: 2,
                placePieceRequired: true,
                pieces: [
                    {type: 'KING', color: 'BLACK', square: 1},
                    {type: 'QUEEN', color: 'WHITE', square: 116}
                ],
                captures: [],
                currentTurn: 'BLACK',
                blackUsername: 'John',
                blackScore: 2,
                whiteUsername: 'Erin',
                whiteScore: 1,
                piecesToBePlaced: [],
                possiblePlacements: []
            });
        });
    },

    getPossibleMoves: function (gameUuid, square) {
        return new Promise((resolve, reject) => {
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
    },

    makeMove: function (gameUuid, move) {
        console.log('Making move');
        console.log(JSON.stringify(move));
        return new Promise((resolve, reject) => resolve('yay'));
    }
};