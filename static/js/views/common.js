function addPiece(squareDivElement, piece) {
    var pieceImgElement = document.createElement('img');
    pieceImgElement.className = 'piece';
    pieceImgElement.src = getPieceImage(piece);
    squareDivElement.appendChild(pieceImgElement);
}

function clearPieceGrid(pieceGridElement) {
    var boardTableBodyElements = pieceGridElement.getElementsByTagName('tbody');
    for (var i = 0; i < boardTableBodyElements.length; ++i) {
        pieceGridElement.removeChild(boardTableBodyElements[i]);
    }
}

function redrawPiecesOnGrid(gridShape, gridElement, pieceList, squareClassName, clickCallback) {
    var pieceIndex = 0;

    for (var i = 0; i < gridShape.rows; ++i) {
        var rowElement = gridElement.insertRow(-1);

        for (var j = 0; j < gridShape.columns; ++j) {
            var cellElement = rowElement.insertCell(-1);
            var squareDiv = document.createElement('div');
            cellElement.className += squareClassName;
            cellElement.appendChild(squareDiv);


            if (pieceIndex < pieceList.length) {
                cellElement.className += ' piece-square';

                let piece = pieceList[pieceIndex++];
                addPiece(squareDiv, piece);

                if (clickCallback != null) {
                    cellElement.onclick = () => clickCallback(piece);
                }
            }
        }
    }
}

function drawGridOfPieces(gridShape, elementId, shouldRedraw, pieceList, squareClassName, clickCallback) {
    var pieceGridElement = document.getElementById(elementId);
    clearPieceGrid(pieceGridElement);

    if (shouldRedraw) {
        redrawPiecesOnGrid(gridShape, pieceGridElement, pieceList, squareClassName, clickCallback);
    }
}
