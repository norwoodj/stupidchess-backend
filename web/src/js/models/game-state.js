export default class GameState {
    constructor() {
        this.pieces = new Map();
        this.gameType = 'NONE';
        this.captures = [];
        this.currentTurn = 'BLACK';
        this.blackUsername = 'Black';
        this.whiteUsername = 'White';
        this.blackScore = 0;
        this.whiteScore = 0;
        this.piecesToBePlaced = [];
        this.possiblePlacements = [];
    }

    hasPieceOnSquare(square) {
        return this.pieces.has(square);
    }

    getPieceOnSquare(square) {
        return this.pieces.get(square);
    }

    mustPlacePiece() {
        return this.piecesToBePlaced.length > 0;
    }

    inBoardSetupMode() {
        return this.mustPlacePiece() && this.piecesToBePlaced.length > 1;
    }

    getColorsSettingUp() {
        var blackPiece = false;
        var whitePiece = false;
        var colorsSettingUp = [];

        this.piecesToBePlaced.forEach(piece => {
            if (piece.color == 'BLACK' && !blackPiece) {
                colorsSettingUp[colorsSettingUp.length] = 'BLACK';
                blackPiece = true;
            } else if (piece.color == 'WHITE' && !whitePiece) {
                colorsSettingUp[colorsSettingUp.length] = 'WHITE';
                whitePiece = true;
            }
        });

        return colorsSettingUp;
    }

    updateFromApiResponse(apiResponse) {
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
}
