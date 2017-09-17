class GameState {
    constructor() {
        this.pieces = new Map();
        this.type = "NONE";
        this.captures = [];
        this.currentTurn = "BLACK";
        this.blackUsername = "Black";
        this.whiteUsername = "White";
        this.lastMove = -2;
        this.blackScore = 0;
        this.whiteScore = 0;
        this.possiblePiecesToBePlaced = [];
        this.squaresToBePlaced = new Set();
    }

    hasPieceOnSquare(square) {
        return this.pieces.has(square);
    }

    getPieceOnSquare(square) {
        return this.pieces.get(square);
    }

    mustPlacePiece() {
        return this.squaresToBePlaced.size > 0;
    }

    inBoardSetupMode() {
        return this.type == "STUPID_CHESS" && this.lastMove < 23;
    }

    getColorsSettingUp() {
        var blackPiece = false;
        var whitePiece = false;
        var colorsSettingUp = [];

        this.possiblePiecesToBePlaced.forEach(piece => {
            if (piece.color == "BLACK" && !blackPiece) {
                colorsSettingUp[colorsSettingUp.length] = "BLACK";
                blackPiece = true;
            } else if (piece.color == "WHITE" && !whitePiece) {
                colorsSettingUp[colorsSettingUp.length] = "WHITE";
                whitePiece = true;
            }
        });

        return colorsSettingUp;
    }

    squareNeedsPiecePlaced(square) {
        return this.squaresToBePlaced.has(square);
    }

    updateFromApiResponse(apiResponse) {
        this.type = apiResponse.type;
        this.captures = apiResponse.captures;
        this.currentTurn = apiResponse.currentTurn;
        this.blackUsername = apiResponse.blackUsername;
        this.whiteUsername = apiResponse.whiteUsername;
        this.lastMove = apiResponse.lastMove;
        this.blackScore = apiResponse.blackScore;
        this.whiteScore = apiResponse.whiteScore;
        this.possiblePiecesToBePlaced = apiResponse.possiblePiecesToBePlaced;

        this.pieces.clear();
        apiResponse.pieces.forEach(piece => this.pieces.set(piece.square, piece));

        this.squaresToBePlaced.clear();
        apiResponse.squaresToBePlaced.forEach(square => this.squaresToBePlaced.add(square));
    }
}

export {GameState};
