var PIECE_NAMES = [
    'KING', 'QUEEN', 'BISHOP', 'CASTLE', 'PONY', 'PAWN', 'CHECKER'
];

var PIECE_IMG_MAP = new Map(PIECE_NAMES.map(pieceName => [pieceName, `${pieceName.toLowerCase()}.svg`]));

function getPieceImage(piece) {
    return `/static/img/pieces/${piece.color.toLowerCase()}/${PIECE_IMG_MAP.get(piece.type)}`;
}