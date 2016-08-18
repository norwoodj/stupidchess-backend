import React from 'react';
import getPieceImage from '../factories/piece-factory'
import {getHalfBoardShapeForColor, getBoardShapeForGameType} from '../factories/board-shapes-factory'


export default class Board extends React.Component {
    getBorderForSquare(square) {
        if (this.props.squareSelectionState.isSquarePossibleCapture(square)) {
            return this.props.displayState.getPossibleCaptureBorder();
        } else if (this.props.squareSelectionState.isSquarePossibleMove(square)) {
            return this.props.displayState.getPossibleMoveBorder();
        } else {
            return '';
        }
    }

    getBackgroundForSquare(square) {
        return this.props.squareSelectionState.isSquareSelected(square)
            ? this.props.displayState.getSelectedBackground()
            : this.props.displayState.getSquareColor(square);
    }

    getClassForSquare(square) {
        if (square == null) {
            return '';
        }

        return `square ${this.props.gameState.hasPieceOnSquare(square) ? 'piece-square' : ''}`
    }

    getPieceImageElementForSquare(square) {
        if (!this.props.gameState.hasPieceOnSquare(square)) {
            return '';
        }

        let piece = this.props.gameState.getPieceOnSquare(square);
        return <img className="piece" src={getPieceImage(piece)}/>
    }

    getStyleForSquare(square) {
        if (square == null) {
            return {};
        }

        return {
            background: this.getBackgroundForSquare(square),
            border: this.getBorderForSquare(square)
        }
    }

    render() {
        let boardShape = this.props.gameState.inBoardSetupMode()
            ? getHalfBoardShapeForColor(this.props.boardSetupState.getCurrentBoardBeingSetUp())
            : getBoardShapeForGameType(this.props.gameState.gameType);

        let squareIndex = 0;

        return (
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
        );
    }
}

Board.propTypes = {
    boardSetupState: React.PropTypes.object.isRequired,
    gameState: React.PropTypes.object.isRequired,
    displayState: React.PropTypes.object.isRequired,
    squareSelectionState: React.PropTypes.object.isRequired,
    clickHandler: React.PropTypes.func.isRequired
};
