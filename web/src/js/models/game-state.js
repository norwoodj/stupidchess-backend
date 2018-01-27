import {Color} from "../constants";
import {isGameInBoardSetupMode, isSquareInSetupZoneForColor} from "../util";


export default class GameState {
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

    getUserColor(userUuid) {
        return (userUuid == this.blackPlayerUuid)
            ? Color.BLACK
            : Color.WHITE;
    }

    isMyTurn(userUuid) {
        if (this.inBoardSetupMode()) {
            return true;
        }

        if (this.blackPlayerUuid == this.whitePlayerUuid) {
            return true;
        }

        return this.getUserColor(userUuid) == this.currentTurn;
    }

    mustPlacePiece() {
        return this.squaresToBePlaced.size > 0;
    }

    singleSquareToBePlaced() {
        return this.squaresToBePlaced.size == 1;
    }

    inBoardSetupMode() {
        return isGameInBoardSetupMode(this);
    }

    getColorsSettingUp(userUuid) {
        let colors = [];

        if (isGameInBoardSetupMode(this) && this.squaresToBePlaced.size == 0) {
            return [this.getUserColor(userUuid)];
        }

        for (let c of [Color.BLACK, Color.WHITE]) {
            for (let s of this.squaresToBePlaced) {
                if (isSquareInSetupZoneForColor(c, s)) {
                    colors[colors.length] = c;
                    break;
                }
            }
        }

        return colors;
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
