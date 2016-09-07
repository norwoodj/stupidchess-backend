function getMoveObjectForPieceMove(startSquare, destinationSquare) {
    return {
        type: 'MOVE',
        startSquare: startSquare,
        destinationSquare: destinationSquare
    };
}

function getMoveObjectForPlacePiece(square, piece) {
    return {
        type: 'PLACE',
        piece: piece,
        destinationSquare: square
    };
}

export {getMoveObjectForPieceMove, getMoveObjectForPlacePiece};
