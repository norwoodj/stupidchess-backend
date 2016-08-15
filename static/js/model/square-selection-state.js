function SquareSelectionState() {
    this.selected = null;
    this.possibleMoves = new Set();
    this.possibleCaptures = new Set();
}

SquareSelectionState.prototype = {
    anySquareSelected: function () {
        return this.selected != null;
    },

    isSquareSelected: function (square) {
        return this.selected == square;
    },

    getSelected: function (square) {
        return this.selected;
    },

    setSelected: function (square) {
        this.selected = square;
    },

    isSquarePossibleMove: function (square)  {
        return this.possibleMoves.has(square);
    },

    addPossibleMove: function (square) {
        this.possibleMoves.add(square);
    },

    isSquarePossibleCapture: function (square) {
        return this.possibleCaptures.has(square);
    },

    addPossibleCapture: function (square) {
        this.possibleCaptures.add(square);
    },

    clear: function () {
        this.selected = null;
        this.possibleMoves.clear();
        this.possibleCaptures.clear();
    }
};