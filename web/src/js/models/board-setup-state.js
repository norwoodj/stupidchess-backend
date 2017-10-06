
export default class BoardSetupState {
    constructor() {
        this.setupBoard = null;
    }

    getCurrentBoardBeingSetUp() {
        return this.setupBoard;
    }

    updateFromColorsSettingUp(colorsSettingUp) {
        if (this.setupBoard == null || (colorsSettingUp.length == 1 && colorsSettingUp[0] != this.setupBoard)) {
            this.setupBoard = colorsSettingUp[0].toUpperCase();
        }
    }

    setUpBoard(color) {
        this.setupBoard = color.toUpperCase();
    }
}
