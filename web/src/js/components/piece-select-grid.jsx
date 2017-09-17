import React from "react";
import {PieceGrid} from "./piece-grid";
import {getPieceSelectShapeForSetupMode} from "../factories/board-shapes-factory";


class PieceSelectGrid extends PieceGrid {
    getPieceForIndex(index) {
        if (this.props.gameState.inBoardSetupMode()) {
            var pieces = this.props.gameState.possiblePiecesToBePlaced
                .filter(piece => (piece.color == this.props.boardSetupState.getCurrentBoardBeingSetUp() && piece.index == index));
            return (pieces.length > 0) ? pieces[0] : null;
        } else{
            return this.props.gameState.possiblePiecesToBePlaced[index];
        }
    }

    getDefaultClassName() {
        return "piece-selection";
    }

    shouldDisplay() {
        return this.props.gameState.mustPlacePiece();
    }

    getGridShape() {
        return getPieceSelectShapeForSetupMode(this.props.gameState.inBoardSetupMode());
    }

    getClickHandler() {
        return piece => {
            if (piece != null) {
                this.props.pieceSelectionCallback(piece);
            }
        }
    }
}

PieceSelectGrid.propTypes = {
    gameState: React.PropTypes.object.isRequired,
    boardSetupState: React.PropTypes.object.isRequired,
    pieceSelectionCallback: React.PropTypes.func.isRequired
};

export {PieceSelectGrid};
