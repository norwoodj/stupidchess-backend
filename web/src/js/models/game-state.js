import {Color, GameType} from "../constants";


class GameState {
    constructor() {
        this.pieces = new Map();
        this.type = "NONE";
        this.captures = [];
        this.currentTurn = Color.BLACK;
        this.lastMove = -2;
        this.blackPlayerName = "Black";
        this.whitePlayerName = "White";
        this.blackPlayerUuid = null;
        this.whitePlayerUuid = null;
        this.blackPlayerScore = 0;
        this.whitePlayerScore = 0;
        this.possiblePiecesToBePlaced = [];
        this.squaresToBePlaced = new Set();
        this.lastUpdateTimestamp = "";
        this.gameResult = null;
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
        return this.type == GameType.STUPID_CHESS && this.lastMove < 23;
    }

    getColorsSettingUp() {
        return [Color.BLACK, Color.WHITE];
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
        this.blackPlayerUuid = apiResponse.blackPlayerUuid;
        this.whitePlayerUuid = apiResponse.whitePlayerUuid;
        this.blackPlayerScore = apiResponse.blackPlayerScore;
        this.whitePlayerScore = apiResponse.whitePlayerScore;
        this.possiblePiecesToBePlaced = apiResponse.possiblePiecesToBePlaced;
        this.lastUpdateTimestamp = apiResponse.lastUpdateTimestamp;
        this.gameResult = apiResponse.gameResult;

        this.pieces.clear();
        apiResponse.pieces.forEach(piece => this.pieces.set(piece.square, piece));

        this.squaresToBePlaced.clear();
        apiResponse.squaresToBePlaced.forEach(square => this.squaresToBePlaced.add(square));
    }
}

export {GameState};
