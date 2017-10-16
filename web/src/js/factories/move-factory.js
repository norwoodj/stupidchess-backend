
function getMoveObjectForPieceMove(startSquare, destinationSquare, disambiguatingCapture = null) {
    var move = {
        type: "MOVE",
        startSquare: startSquare,
        destinationSquare: destinationSquare
    };

    if (disambiguatingCapture != null) {
        move.disambiguatingCapture = disambiguatingCapture;
    }

    return move;
}

function getMoveObjectForPlacePiece(square, piece) {
    return {
        type: "PLACE",
        piece: piece,
        destinationSquare: square
    };
}

function getMoveObjectForReplacePiece(square, piece) {
    return {
        type: "REPLACE",
        piece: piece,
        destinationSquare: square
    };
}

export {getMoveObjectForPieceMove, getMoveObjectForPlacePiece, getMoveObjectForReplacePiece};
