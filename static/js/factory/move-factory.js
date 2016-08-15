function getMoveObjectForPieceMove(start, end) {
    return {
        type: 'MOVE',
        start: start,
        end: end
    };
}

function getMoveObjectForPlacePiece(square, piece) {
    return {
        type: 'PLACE',
        piece: piece,
        square: square
    };
}
