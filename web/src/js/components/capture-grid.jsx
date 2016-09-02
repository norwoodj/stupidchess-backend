import React from 'react';
import {PieceGrid} from './piece-grid';
import {getCaptureShapeForGameType} from '../factories/board-shapes-factory';


class CaptureGrid extends PieceGrid {
    getDefaultClassName() {
        return 'capture';
    }

    getPieceList() {
        return this.props.gameState.captures.filter(piece => piece.color == this.props.captureColor);
    }

    shouldDisplay() {
        return !this.props.gameState.inBoardSetupMode();
    }

    getGridShape() {
        return getCaptureShapeForGameType(this.props.gameState.gameType);
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
