import React from "react";
import PropTypes from "prop-types";
import ReactTable from "react-table";
import timeago from "timeago.js";
import {toTitleCase} from "../util";
import {getPieceImage} from "../factories/piece-factory";


export default class MoveList extends React.Component {
    constructor() {
        super();
        this.timeAgo = timeago();
    }

    static getSquaresForMove(move) {
        return move.type == "MOVE" ? `${move.startSquare}=>${move.destinationSquare}` : move.destinationSquare;
    }

    static getCapturesForMove(move) {
        return move.type == "MOVE" && move.captures
            ? move.captures.map((c, idx) => <img key={idx} className="move-list-piece" src={getPieceImage(c)}/>)
            : "";
    }

    getMovesTableColumns() {
        return [
            {Header: "Type", Cell: row => toTitleCase(row.original.type), maxWidth: 65},
            {Header: "Piece", Cell: row => <img className="move-list-piece" src={getPieceImage(row.original.piece)}/>, maxWidth: 50},
            {Header: "Squares", Cell: row => MoveList.getSquaresForMove(row.original), maxWidth: 75},
            {Header: "Captures", Cell: row => MoveList.getCapturesForMove(row.original)},
            {Header: "Time", Cell: row => this.timeAgo.format(row.original.createTimestamp)}
        ];
    }

    render() {
        return (
            <div className="content-block move-table">
                <h3>Last {Math.min(this.props.pagedListState.pageSizeLimit, this.props.pagedListState.objectCount)} Moves</h3>
                <ReactTable
                    manual
                    columns={this.getMovesTableColumns()}
                    sortable={false}
                    loading={this.props.pagedListState.loading}
                    defaultPageSize={this.props.pagedListState.pageSizeLimit}
                    pageSizeOptions={this.props.pagedListState.pageSizeOptions}
                    pages={this.props.pagedListState.pages}
                    data={this.props.pagedListState.objects}
                    onPageChange={this.props.handlePageChangeFn}
                    onPageSizeChange={this.props.handlePageSizeChangeFn}
                />
            </div>
        );
    }
}

MoveList.propTypes = {
    pagedListState: PropTypes.object.isRequired,
    handlePageChangeFn: PropTypes.func.isRequired,
    handlePageSizeChangeFn: PropTypes.func.isRequired
};
