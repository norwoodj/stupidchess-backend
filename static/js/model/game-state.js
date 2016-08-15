function GameState() {
    this.pieces = new Map();
}

GameState.prototype = {
    hasPieceOnSquare: function (square) {
        return this.pieces.has(square);
    },

    getPieceOnSquare: function (square) {
        return this.pieces.get(square);
    },

    mustPlacePiece: function () {
        return this.piecesToBePlaced.length > 0;
    },

    inBoardSetupMode: function () {
        return this.mustPlacePiece() && this.piecesToBePlaced.length > 1;
    },

    getColorsSettingUp: function () {
        var blackPiece = false;
        var whitePiece = false;
        var colorsSettingUp = [];

        this.piecesToBePlaced.forEach(piece => {
            if (piece.color == 'BLACK' && !blackPiece) {
                colorsSettingUp[colorsSettingUp.length] = 'BLACK';
                blackPiece = true;
            } else if (piece.color == 'WHITE') {
                colorsSettingUp[colorsSettingUp.length] = 'WHITE';
                whitePiece = true;
            }
        });

        return colorsSettingUp;
    },

    updateFromApiResponse: function (apiResponse) {
        this.gameType = apiResponse.gameType;
        this.captures = apiResponse.captures;
        this.currentTurn = apiResponse.currentTurn;
        this.blackUsername = apiResponse.blackUsername;
        this.whiteUsername = apiResponse.whiteUsername;
        this.blackScore = apiResponse.blackScore;
        this.whiteScore = apiResponse.whiteScore;
        this.piecesToBePlaced = apiResponse.piecesToBePlaced;
        this.possiblePlacements = apiResponse.possiblePlacements;

        this.pieces.clear();
        apiResponse.pieces.forEach(piece => this.pieces.set(piece.square, piece));
    }
};