(function () {

    var SQUARE_COLOR_CLASSES = ['black-square', 'white-square'];

    function drawCell(rowElement, square, squareIndex) {
        var cellElement = rowElement.insertCell(-1);
        cellElement.className += ' square';
        if (square != null) {
            cellElement.className += ' ' + SQUARE_COLOR_CLASSES[squareIndex % 2];
        }
    }

    function drawRow(boardElement, rowSquares, rowIndex) {
        var rowElement = boardElement.insertRow(-1);

        for (var i = 0; i < rowSquares.length; ++i) {
            drawCell(rowElement, rowSquares[i], i + rowIndex)
        }

    }

    function drawBoard(boardState) {
        var boardElement = document.getElementById('board');
        var rows = boardElement.getElementsByTagName('tr');

        for (var i = 0; i < rows.length; ++i) {
            boardElement.removeChild(rows[i]);
        }

        for (var i = 0; i < boardState.length; ++i) {
            drawRow(boardElement, boardState[i], i);
        }
    }

    window.onload = function () {
        var boardState = [
            [{}, {}, {}, {}, null, null, null, null],
            [{}, {}, {}, {}, null, null, null, null],
            [{}, {}, {}, {}, null, null, null, null],
            [{}, {}, {}, {}, null, null, null, null],
            [{}, {}, {}, {}, {}, {}, {}, {}],
            [{}, {}, {}, {}, {}, {}, {}, {}],
            [{}, {}, {}, {}, {}, {}, {}, {}],
            [{}, {}, {}, {}, {}, {}, {}, {}],
            [null, null, null, null, {}, {}, {}, {}],
            [null, null, null, null, {}, {}, {}, {}],
            [null, null, null, null, {}, {}, {}, {}],
            [null, null, null, null, {}, {}, {}, {}]
        ];

        drawBoard(boardState);
    };
})();
