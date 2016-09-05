import React from 'react';
import {PieceGrid} from './piece-grid';
import {getPieceSelectShapeForSetupMode} from '../factories/board-shapes-factory';


class PieceSelectGrid extends PieceGrid {
    getDefaultClassName() {
        return 'piece-selection';
    }

    getPieceList() {
        return this.props.gameState.inBoardSetupMode()
            ? this.props.gameState.possiblePiecesToBePlaced.filter(piece => piece.color == this.props.boardSetupState.getCurrentBoardBeingSetUp())
            : this.props.gameState.possiblePiecesToBePlaced;
    }

    shouldDisplay() {
        return this.props.gameState.mustPlacePiece();
    }

    getGridShape() {
        return getPieceSelectShapeForSetupMode(this.props.gameState.inBoardSetupMode());
    }

    getClickHandler() {
        return piece => this.props.pieceSelectionCallback(piece);
    }
}

PieceSelectGrid.propTypes = {
    gameState: React.PropTypes.object.isRequired,
    boardSetupState: React.PropTypes.object.isRequired,
    pieceSelectionCallback: React.PropTypes.func.isRequired
};

export {PieceSelectGrid};
