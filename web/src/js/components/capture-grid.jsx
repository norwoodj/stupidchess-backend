import PropTypes from "prop-types";
import PieceGrid from "./piece-grid";
import {getCaptureShapeForGameType} from "../factories/board-shapes-factory";


export default class CaptureGrid extends PieceGrid {
    getPieceForIndex(index) {
        let piecesForColor = this.props.gameState.captures.filter(piece => piece.color == this.props.captureColor);
        return (piecesForColor.length > index) ? piecesForColor[index] : null;
    }

    getSquareClassName() {
        return "capture";
    }

    getGridClassName() {
        return "content-block mui-col-lg-12 mui-col-md-12 mui-col-sm-6 mui-col-xs-6";
    }

    shouldDisplay() {
        return !this.props.gameState.mustPlacePiece();
    }

    getGridShape() {
        return getCaptureShapeForGameType(this.props.gameState.type);
    }

    getClickHandler() {
        return () => {};
    }

}

CaptureGrid.propTypes = {
    color: PropTypes.string.isRequired,
    gameState: PropTypes.object.isRequired,
    captureColor: PropTypes.string.isRequired
};
