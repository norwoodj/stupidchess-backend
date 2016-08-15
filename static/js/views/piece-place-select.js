function drawPieceSelections(gameState, boardSetupState, pieceClickCallback) {
    var gridShape = getPieceSelectShapeForSetupMode(gameState.inBoardSetupMode());

    var piecesToPlace = gameState.inBoardSetupMode()
        ? gameState.piecesToBePlaced.filter(piece => piece.color == boardSetupState.getCurrentBoardBeingSetUp())
        : gameState.piecesToBePlaced;

    drawGridOfPieces(gridShape, 'piece-select', gameState.mustPlacePiece(), piecesToPlace, 'piece-selection', pieceClickCallback);
}