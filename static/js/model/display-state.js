function DisplayState() {
    this.squareColors = ['saddlebrown', 'sandybrown'];
    this.possibleMoveColor = 'yellow';
    this.possibleCaptureColor = 'red';
    this.selectedColor = 'green';
}

DisplayState.prototype = {
    getSquareColor: function (location) {
        var rowIndex = Math.floor(location / 10);
        return this.squareColors[(rowIndex + location) % 2];
    },

    getSelectedBackground: function () {
        return this.selectedColor;
    },

    getPossibleMoveBorder: function () {
        return `2px dashed ${this.possibleMoveColor}`;
    },

    getPossibleCaptureBorder: function () {
        return `2px solid ${this.possibleCaptureColor}`;
    }
};
