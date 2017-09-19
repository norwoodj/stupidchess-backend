import React from "react";
import {PieceGrid} from "./piece-grid";
import {getCaptureShapeForGameType} from "../factories/board-shapes-factory";


class CaptureGrid extends PieceGrid {
    getDefaultClassName() {
        return "capture";
    }

    getPieceForIndex(index) {
        let piecesForColor = this.props.gameState.captures.filter(piece => piece.color == this.props.captureColor);
        return (piecesForColor.length > index) ? piecesForColor[index] : null;
    }

    shouldDisplay() {
        return !this.props.gameState.inBoardSetupMode();
    }

    getGridShape() {
        return getCaptureShapeForGameType(this.props.gameState.type);
    }

    getClickHandler() {
        return () => {
        };
    }

}

CaptureGrid.propTypes = {
    gameState: React.PropTypes.object.isRequired,
    captureColor: React.PropTypes.string.isRequired
};

export {CaptureGrid};
