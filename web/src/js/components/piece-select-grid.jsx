import PropTypes from "prop-types";
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
        return piece => (piece != null) ? this.props.pieceSelectionCallback(piece) : null;
    }
}

PieceSelectGrid.propTypes = {
    gameState: PropTypes.object.isRequired,
    boardSetupState: PropTypes.object.isRequired,
    pieceSelectionCallback: PropTypes.func.isRequired
};

export {PieceSelectGrid};
