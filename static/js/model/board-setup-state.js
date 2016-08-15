
function BoardSetupState() {
    this.setupBoard = null;
}

BoardSetupState.prototype = {
    getCurrentBoardBeingSetUp: function () {
        return this.setupBoard;
    },

    setUpBoard: function (color) {
        this.setupBoard = color;
    },

    isBoardBeingSetUp: function () {
        return this.setupBoard != null;
    },

    reset: function() {
        this.setupBoard = null;
    }
};
