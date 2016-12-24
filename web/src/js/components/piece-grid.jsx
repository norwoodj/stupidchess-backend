import React from 'react';
import getPieceImage from '../factories/piece-factory';
import {range} from '../util';


class PieceGridSquare extends React.Component {
    getSquareClassName() {
        return `${this.props.defaultClass} ${this.props.piece != null ? 'piece-square' : ''}`;
    }

    getPieceImage() {
        return this.props.piece != null ? <img className="piece" src={getPieceImage(this.props.piece)}/> : ''
    }

    render() {
        console.log('PieceGridSquare');
        return (
            <td className={this.getSquareClassName()} onClick={this.props.clickHandler}>
                <div>{this.getPieceImage()}</div>
            </td>
        );
    }
}

PieceGridSquare.propTypes = {
    piece: React.PropTypes.object,
    defaultClass: React.PropTypes.string.isRequired,
    clickHandler: React.PropTypes.func.isRequired
};


class PieceGrid extends React.Component {
    getPieceGridSquareForIndices(rowIndex, cellIndex, gridShape) {
        let index = rowIndex * gridShape.columns + cellIndex;
        let piece = this.getPieceForIndex(index);
        let clickHandler = this.getClickHandler();

        return (
            <PieceGridSquare
                key={index}
                defaultClass={this.getDefaultClassName()}
                piece={piece}
                clickHandler={() => clickHandler(piece)}
            />
        );
    }

    render() {
        console.log('PieceGrid');
        if (!this.shouldDisplay()) {
            return null;
        }

        let gridShape = this.getGridShape();

        return (
            <div className="content-block mui-col-md-12 mui-col-sm-6 mui-col-xs-6">
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

export {PieceGrid};
