
class AbstractDisplayState {
    getSquareColor(square) {
        let rowIndex = Math.floor(square / 10);
        let squareColors = this.getSquareColors();
        return squareColors[(rowIndex + square) % 2];
    }

    getCaptureGridColor() {
        return "green";
    }

    getPieceSelectGridColor() {
        return "green";
    }

    getSelectedBackground() {
        return "green";
    }

    getPossibleMoveBackground() {
        return "yellow";
    }

    getSquareNeedsPlacedBackground() {
        return "yellow";
    }

    getPossibleCaptureBackground() {
        return "red";
    }

    getGamePanelStyle() {
        return {
            backgroundImage: `url(${this.getGamePanelBackgroundImage()})`,
            WebkitBackgroundSize: "cover",
            MozBackgroundSize: "cover",
            OBackgroundSize: "cover",
            backgroundSize: "cover"
        };
    }
}


class DefaultDisplayState extends AbstractDisplayState {
    getSquareColors() {
        return ["saddlebrown", "sandybrown"];
    }

    getGamePanelBackgroundImage() {
        return "/img/themes/wood.jpg";
    }
}

class MichiganDisplayState extends AbstractDisplayState {
    getCaptureGridColor() {
        return "yellow";
    }

    getPieceSelectGridColor() {
        return "yellow";
    }

    getSquareColors() {
        return ["navy", "yellow"];
    }

    getGamePanelBackgroundImage() {
        return "/img/themes/michigan.jpg";
    }

    getPossibleMoveBackground() {
        return "gray";
    }

    getSquareNeedsPlacedBackground() {
        return "gray";
    }
}

class ChristmasDisplayState extends AbstractDisplayState {
    getCaptureGridColor() {
        return "red";
    }

    getPieceSelectGridColor() {
        return "red";
    }

    getSquareColors() {
        return ["red", "green"];
    }

    getGamePanelBackgroundImage() {
        return "/img/themes/snow.jpg";
    }

    getSelectedBackground() {
        return "white";
    }

    getPossibleCaptureBackground() {
        return "navy";
    }
}

let DISPLAY_STATES_BY_NAME = new Map();
DISPLAY_STATES_BY_NAME.set("Default", DefaultDisplayState);
DISPLAY_STATES_BY_NAME.set("Michigan", MichiganDisplayState);
DISPLAY_STATES_BY_NAME.set("Christmas", ChristmasDisplayState);

let DISPLAY_STATES_OPTIONS = ["Default", "Michigan", "Christmas"];

export {DISPLAY_STATES_BY_NAME, DISPLAY_STATES_OPTIONS, DefaultDisplayState};
