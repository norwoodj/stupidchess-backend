import React from "react";
import PropTypes from "prop-types";
import {getPieceImage} from "../factories/piece-factory";
import {range} from "../util";


class PieceGridSquare extends React.Component {
    getSquareClassName() {
        return `${this.props.defaultClass} ${this.props.piece != null ? "piece-square" : ""}`;
    }

    getPieceImage() {
        return this.props.piece != null ? <img className="piece" src={getPieceImage(this.props.piece)}/> : "";
    }

    render() {
        return (
            <td className={this.getSquareClassName()} style={{background: this.props.color}} onClick={this.props.clickHandler}>
                <div>{this.getPieceImage()}</div>
            </td>
        );
    }
}

PieceGridSquare.propTypes = {
    color: PropTypes.string.isRequired,
    piece: PropTypes.object,
    defaultClass: PropTypes.string.isRequired,
    clickHandler: PropTypes.func.isRequired
};


export default class PieceGrid extends React.Component {
    getPieceGridSquareForIndices(rowIndex, cellIndex, gridShape) {
        let index = rowIndex * gridShape.columns + cellIndex;
        let piece = this.getPieceForIndex(index);
        let clickHandler = this.getClickHandler();

        return (
            <PieceGridSquare
                key={index}
                color={this.props.color}
                defaultClass={this.getSquareClassName()}
                piece={piece}
                clickHandler={() => clickHandler(piece)}
            />
        );
    }

    render() {
        if (!this.shouldDisplay()) {
            return null;
        }

        let gridShape = this.getGridShape();

        return (
            <div className={this.getGridClassName()}>
                <table className="piece-grid non-board-grid">
                    <tbody>{ range(gridShape.rows).map(rowIndex => (
                        <tr key={rowIndex}>{ range(gridShape.columns).map(cellIndex => (
                            this.getPieceGridSquareForIndices(rowIndex, cellIndex, gridShape)
                        ))}</tr>
                    ))}</tbody>
                </table>
            </div>
        );
    }
}

PieceGrid.propTypes = {
    color: PropTypes.string.isRequired
};
