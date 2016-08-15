function drawCell(gameState, pieceSelectionState, displayState, clickCallback, rowElement, square) {
    var squareDiv = document.createElement('div');
    var cellElement = rowElement.insertCell(-1);
    cellElement.appendChild(squareDiv);

    if (square != null) {
        cellElement.className = 'square';
        cellElement.style.background = displayState.getSquareColor(square);
        var piece = gameState.getPieceOnSquare(square);
        if (piece != null) {
            cellElement.className += ' piece-square';
            addPiece(squareDiv, piece)
        }

        if (pieceSelectionState.isSquareSelected(square)) {
            cellElement.style.backgroundColor = displayState.getSelectedBackground();
        } else if (pieceSelectionState.isSquarePossibleCapture(square)) {
            cellElement.style.border = displayState.getPossibleCaptureBorder();
        } else if (pieceSelectionState.isSquarePossibleMove(square)) {
            cellElement.style.border = displayState.getPossibleMoveBorder();
        }

        cellElement.onclick = e => clickCallback(square);
    }
}

function drawRow(gameState, pieceSelectionState, displayState, clickCallback, boardElement, rowSquares) {
    var rowElement = boardElement.insertRow(-1);

    for (var i = 0; i < rowSquares.length; ++i) {
        drawCell(gameState, pieceSelectionState, displayState, clickCallback, rowElement, rowSquares[i]);
    }
}

function drawBoard(gameState, pieceSelectionState, displayState, boardSetupState, clickCallback) {
    var boardElement = document.getElementById('board');
    clearPieceGrid(boardElement);

    var boardShape = boardSetupState.isBoardBeingSetUp()
        ? getHalfBoardShapeForColor(boardSetupState.getCurrentBoardBeingSetUp())
        : getBoardShapeForGameType(gameState.gameType);

    for (var i = 0; i < boardShape.length; ++i) {
        drawRow(gameState, pieceSelectionState, displayState, clickCallback, boardElement, boardShape[i]);
    }
}
