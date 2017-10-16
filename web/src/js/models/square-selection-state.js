
export default class SquareSelectionState {
    constructor() {
        this.selected = null;
        this.possibleMoves = new Set();
        this.possibleCaptures = new Set();
    }

    anySquareSelected() {
        return this.selected != null;
    }

    isSquareSelected(square) {
        return this.selected == square;
    }

    getSelected() {
        return this.selected;
    }

    setSelected(square) {
        this.selected = square;
    }

    isSquarePossibleMove(square)  {
        return this.possibleMoves.has(square);
    }

    addPossibleMove(square) {
        this.possibleMoves.add(square);
    }

    isSquarePossibleCapture(square) {
        return this.possibleCaptures.has(square);
    }

    addPossibleCapture(square) {
        this.possibleCaptures.add(square);
    }

    clear() {
        this.selected = null;
        this.possibleMoves.clear();
        this.possibleCaptures.clear();
    }
}
