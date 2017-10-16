import {GameType, Color} from "../constants";


let STUPID_CHESS_BOARD = [
    [   0,    1,    2,    3, null, null, null, null],
    [  10,   11,   12,   13, null, null, null, null],
    [  20,   21,   22,   23, null, null, null, null],
    [  30,   31,   32,   33, null, null, null, null],
    [  40,   41,   42,   43,   44,   45,   46,   47],
    [  50,   51,   52,   53,   54,   55,   56,   57],
    [  60,   61,   62,   63,   64,   65,   66,   67],
    [  70,   71,   72,   73,   74,   75,   76,   77],
    [null, null, null, null,   84,   85,   86,   87],
    [null, null, null, null,   94,   95,   96,   97],
    [null, null, null, null,  104,  105,  106,  107],
    [null, null, null, null,  114,  115,  116,  117]
];

let NORMAL_CHESS_BOARD = [
    [ 0,  1,  2,  3,  4,  5,  6,  7],
    [10, 11, 12, 13, 14, 15, 16, 17],
    [20, 21, 22, 23, 24, 25, 26, 27],
    [30, 31, 32, 33, 34, 35, 36, 37],
    [40, 41, 42, 43, 44, 45, 46, 47],
    [50, 51, 52, 53, 54, 55, 56, 57],
    [60, 61, 62, 63, 64, 65, 66, 67],
    [70, 71, 72, 73, 74, 75, 76, 77]
];

let STUPID_CHESS_BLACK_HALF_BOARD = [
    [null,   73,   72,   71,   70, null],
    [null,   63,   62,   61,   60, null],
    [null,   53,   52,   51,   50, null],
    [null,   43,   42,   41,   40, null],
    [null,   33,   32,   31,   30, null],
    [null,   23,   22,   21,   20, null],
    [null,   13,   12,   11,   10, null],
    [null,    3,    2,    1,    0, null],
    [null, null, null, null, null, null]
];

let STUPID_CHESS_WHITE_HALF_BOARD = [
    [null,   44,   45,   46,   47, null],
    [null,   54,   55,   56,   57, null],
    [null,   64,   65,   66,   67, null],
    [null,   74,   75,   76,   77, null],
    [null,   84,   85,   86,   87, null],
    [null,   94,   95,   96,   97, null],
    [null,  104,  105,  106,  107, null],
    [null,  114,  115,  116,  117, null],
    [null, null, null, null, null, null]
];

let STUPID_CHESS_CAPTURES = {rows: 3, columns: 4};
let NORMAL_CHESS_CAPTURES = {rows: 3, columns: 6};

let STUPID_CHESS_PIECE_SETUP_SELECTION_SHAPE = STUPID_CHESS_CAPTURES;
let STUPID_CHESS_REPLACE_PIECE_SELECTION_SHAPE = STUPID_CHESS_CAPTURES;
let CHESS_REPLACE_PIECE_SELECTION_SHAPE = NORMAL_CHESS_CAPTURES;

let BOARD_SHAPE_FOR_GAME_TYPE = new Map([
    [GameType.STUPID_CHESS, STUPID_CHESS_BOARD],
    [GameType.CHESS, NORMAL_CHESS_BOARD],
    [GameType.CHECKERS, NORMAL_CHESS_BOARD],
    ["NONE", []]
]);

let CAPTURE_SHAPE_FOR_GAME_TYPE = new Map([
    [GameType.STUPID_CHESS, STUPID_CHESS_CAPTURES],
    [GameType.CHESS, NORMAL_CHESS_CAPTURES],
    [GameType.CHECKERS, NORMAL_CHESS_CAPTURES],
    ["NONE", {rows: 0, columns: 0}]
]);

let HALF_BOARD_SHAPE_FOR_COLOR = new Map([
    [Color.BLACK, STUPID_CHESS_BLACK_HALF_BOARD],
    [Color.WHITE, STUPID_CHESS_WHITE_HALF_BOARD],
    ["NONE", []]
]);


function getHalfBoardShapeForColor(color) {
    return HALF_BOARD_SHAPE_FOR_COLOR.get(color);
}

function getBoardShapeForGameType(gameType) {
    return BOARD_SHAPE_FOR_GAME_TYPE.get(gameType);
}

function getCaptureShapeForGameType(gameType) {
    return CAPTURE_SHAPE_FOR_GAME_TYPE.get(gameType);
}

function getPieceSelectShapeForGameTypeAndSetupMode(gameType, inSetupMode) {
    if (gameType == GameType.CHESS) {
        return CHESS_REPLACE_PIECE_SELECTION_SHAPE;
    }

    return inSetupMode
        ? STUPID_CHESS_PIECE_SETUP_SELECTION_SHAPE
        : STUPID_CHESS_REPLACE_PIECE_SELECTION_SHAPE;
}

export {
    getBoardShapeForGameType,
    getHalfBoardShapeForColor,
    getCaptureShapeForGameType,
    getPieceSelectShapeForGameTypeAndSetupMode
};
