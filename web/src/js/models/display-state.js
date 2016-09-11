export default class DisplayState {
    constructor() {
        this.squareColors = ['saddlebrown', 'sandybrown'];
        this.possibleMoveColor = 'yellow';
        this.possibleCaptureColor = 'red';
        this.selectedColor = 'green';
    }

    getSquareColor(square) {
        var rowIndex = Math.floor(square / 10);
        return this.squareColors[(rowIndex + square) % 2]
    }

    getSelectedBackground() {
        return this.selectedColor;
    }

    getPossibleMoveBackground() {
        return this.possibleMoveColor;
    }

    getPossibleCaptureBackground() {
        return this.possibleCaptureColor;
    }
}
