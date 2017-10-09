import PropTypes from "prop-types";
import PieceGrid from "./piece-grid";
import {getPieceSelectShapeForGameTypeAndSetupMode} from "../factories/board-shapes-factory";


export default class PieceSelectGrid extends PieceGrid {
    getPieceForIndex(index) {
        if (this.props.gameState.inBoardSetupMode()) {
            let pieces = this.props.gameState.possiblePiecesToBePlaced
                .filter(piece => (piece.color == this.props.boardSetupState.getCurrentBoardBeingSetUp() && piece.index == index));
            return (pieces.length > 0) ? pieces[0] : null;
        } else{
            return this.props.gameState.possiblePiecesToBePlaced[index];
        }
    }

    getSquareClassName() {
        return "piece-selection";
    }

    getGridClassName() {
        return "content-block";
    }

    shouldDisplay() {
        return this.props.gameState.mustPlacePiece();
    }

    getGridShape() {
        return getPieceSelectShapeForGameTypeAndSetupMode(
            this.props.gameState.type,
            this.props.gameState.inBoardSetupMode()
        );
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
