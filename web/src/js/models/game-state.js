import {Color} from "../constants";


class GameState {
    constructor() {
        this.pieces = new Map();
        this.type = "NONE";
        this.captures = [];
        this.currentTurn = Color.BLACK;
        this.lastMove = -2;
        this.blackPlayerName = "Black";
        this.whitePlayerName = "White";
        this.blackPlayerScore = 0;
        this.whitePlayerScore = 0;
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
        let blackPiece = false;
        let whitePiece = false;
        let colorsSettingUp = [];

        this.possiblePiecesToBePlaced.forEach(piece => {
            if (piece.color == Color.BLACK && !blackPiece) {
                colorsSettingUp[colorsSettingUp.length] = Color.BLACK;
                blackPiece = true;
            } else if (piece.color == Color.WHITE && !whitePiece) {
                colorsSettingUp[colorsSettingUp.length] = Color.WHITE;
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
        this.lastMove = apiResponse.lastMove;
        this.blackPlayerName = apiResponse.blackPlayerName;
        this.whitePlayerName = apiResponse.whitePlayerName;
        this.blackPlayerScore = apiResponse.blackPlayerScore;
        this.whitePlayerScore = apiResponse.whitePlayerScore;
        this.possiblePiecesToBePlaced = apiResponse.possiblePiecesToBePlaced;

        this.pieces.clear();
        apiResponse.pieces.forEach(piece => this.pieces.set(piece.square, piece));

        this.squaresToBePlaced.clear();
        apiResponse.squaresToBePlaced.forEach(square => this.squaresToBePlaced.add(square));
    }
}

export {GameState};
