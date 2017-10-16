import React from "react";
import PropTypes from "prop-types";
import {getPieceImage} from "../factories/piece-factory";
import {getHalfBoardShapeForColor, getBoardShapeForGameType} from "../factories/board-shapes-factory";


export default class Board extends React.Component {
    getBackgroundForSquare(square) {
        if (this.props.squareSelectionState.isSquareSelected(square)) {
            return this.props.displayState.getSelectedBackground();
        } else if (this.props.gameState.squareNeedsPiecePlaced(square)) {
            return this.props.displayState.getSquareNeedsPlacedBackground();
        } else if (this.props.ambiguousMoveState.isAmbiguousDestinationSelected()) {
            if (this.props.ambiguousMoveState.getSelectedAmbiguousDestination() == square) {
                return this.props.displayState.getPossibleMoveBackground();
            } else if (this.props.ambiguousMoveState.isDisambiguatingCaptureForSelectedSquare(square)) {
                return this.props.displayState.getPossibleCaptureBackground();
            }
        } else if (this.props.squareSelectionState.isSquarePossibleCapture(square)) {
            return this.props.displayState.getPossibleCaptureBackground();
        } else if (this.props.squareSelectionState.isSquarePossibleMove(square)) {
            return this.props.displayState.getPossibleMoveBackground();
        }

        return this.props.displayState.getSquareColor(square);
    }

    getClassForSquare(square) {
        if (square == null) {
            return "";
        }

        return `square ${this.props.gameState.hasPieceOnSquare(square) ? "piece-square" : ""}`;
    }

    getPieceImageElementForSquare(square) {
        if (!this.props.gameState.hasPieceOnSquare(square)) {
            return "";
        }

        let piece = this.props.gameState.getPieceOnSquare(square);
        return <img className="piece" src={getPieceImage(piece)}/>;
    }

    getStyleForSquare(square) {
        if (square == null) {
            return {};
        }

        return {
            background: this.getBackgroundForSquare(square)
        };
    }

    render() {
        let boardShape = this.props.gameState.inBoardSetupMode()
            ? getHalfBoardShapeForColor(this.props.boardSetupState.getCurrentBoardBeingSetUp())
            : getBoardShapeForGameType(this.props.gameState.type);

        let squareIndex = 0;

        return (
            <div id="board-block" className="content-block mui-col-md-7 mui-col-sm-12">
                <table id="board" className="piece-grid">
                    <tbody>{ boardShape.map((row, rowIndex) => (
                        <tr key={rowIndex}>{ row.map(square => (
                            <td key={squareIndex++}
                                className={this.getClassForSquare(square)}
                                style={this.getStyleForSquare(square)}
                                onClick={() => this.props.clickHandler(square)}
                            >
                                <div>{this.getPieceImageElementForSquare(square)}</div>
                            </td>
                        ))}</tr>
                    ))}</tbody>
                </table>
            </div>
        );
    }
}

Board.propTypes = {
    boardSetupState: PropTypes.object.isRequired,
    gameState: PropTypes.object.isRequired,
    displayState: PropTypes.object.isRequired,
    squareSelectionState: PropTypes.object.isRequired,
    ambiguousMoveState: PropTypes.object.isRequired,
    clickHandler: PropTypes.func.isRequired
};
