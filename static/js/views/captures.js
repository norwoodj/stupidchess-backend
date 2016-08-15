function drawCaptures(gameState) {
    var capturesShape = getCaptureShapeForGameType(gameState.gameType);
    var blackCaptures = gameState.captures.filter(piece => piece.color == 'BLACK');
    var whiteCaptures = gameState.captures.filter(piece => piece.color == 'WHITE');

    drawGridOfPieces(capturesShape, 'black-captures', !gameState.inBoardSetupMode(), blackCaptures, 'capture');
    drawGridOfPieces(capturesShape, 'white-captures', !gameState.inBoardSetupMode(), whiteCaptures, 'capture');
}
