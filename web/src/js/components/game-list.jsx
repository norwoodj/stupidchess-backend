import React from "react";
import PropTypes from "prop-types";
import ReactTable from "react-table";
import PagedListState from "../models/paged-list-state";
import UpdatingSelect from "../components/updating-select";

import {Color, GameType} from "../constants";
import {toTitleCase} from "../util";
import timeago from "timeago.js";


export default class GameList extends React.Component {
    constructor() {
        super();

        this.pagedListState = new PagedListState();
        this.state = {
            selectedGameType: "ALL",
            pagedListState: this.pagedListState
        };

        this.timeAgo = timeago();
    }

    componentDidMount() {
        this.setState({pagedListState: this.pagedListState});
        this.retrieveGames(this.state.pagedListState.pageStartOffset, this.state.pagedListState.pageSizeLimit);
        this.retrieveGameCount();
    }

    getUuidLinkClassName() {
        return "uuid-link";
    }

    getOtherPlayerLinkClassName() {
        return "";
    }

    getUuidLinkElementForGame(game) {
        return <a className={this.getUuidLinkClassName()} href={`/game?gameUuid=${game.id}`}>{game.id}</a>;
    }

    getUserColor(game) {
        if (this.props.userUuid == game.blackPlayerUuid) {
            return Color.BLACK;
        } else {
            return Color.WHITE;
        }
    }

    getOpponentNameElement(game) {
        let myColor = this.getUserColor(game);
        let className = this.getOtherPlayerLinkClassName();

        if (game.blackPlayerUuid != game.whitePlayerUuid) {
            if (myColor == Color.BLACK) {
                return <a className={className} href={`/profile?userUuid=${game.whitePlayerUuid}`}>{game.whitePlayerName}</a>;
            } else {
                return <a className={className} href={`/profile?userUuid=${game.blackPlayerUuid}`}>{game.blackPlayerName}</a>;
            }
        } else {
            return (myColor == Color.BLACK) ? game.whitePlayerName : game.blackPlayerName;
        }
    }

    getUserColorElement(game) {
        let myColor = this.getUserColor(game);
        return <div className={`color-label-${myColor.toLowerCase()}`}>{toTitleCase(myColor)}</div>;
    }

    retrieveGameCount() {
        let gameType = (this.state.selectedGameType == "ALL") ? null : this.state.selectedGameType;

        this.doRetrieveGameCount(gameType).then((gameCount) => {
            this.pagedListState.updateForObjectCount(gameCount);
            this.setState(this.pagedListState);
        });
    }

    retrieveGames() {
        let gameType = (this.state.selectedGameType == "ALL") ? null : this.state.selectedGameType;

        this.doRetrieveGames(gameType, this.state.pagedListState.pageStartOffset, this.state.pagedListState.pageSizeLimit).then(games => {
            this.pagedListState.updateForObjects(games);
            this.setState(this.pagedListState);
        });
    }

    handlePageChange(page) {
        this.pagedListState.handlePageChange(page);
        this.setState(this.pagedListState, () => this.retrieveGames());
    }

    handlePageSizeChange(pageSize, page) {
        this.pagedListState.handlePageSizeChange(pageSize, page);
        this.setState(this.pagedListState, () => this.retrieveGames());
    }

    getGamesTableColumns() {
        return [
            {Header: "ID", Cell: row => this.getUuidLinkElementForGame(row.original)},
            {Header: "Game Type", Cell: row => toTitleCase(row.original.type)},
            {Header: "User Color", Cell: row => this.getUserColorElement(row.original)},
            {Header: "Opponent", Cell: row => this.getOpponentNameElement(row.original, "")},
            {Header: "Black Score", Cell: row => row.original.blackPlayerScore},
            {Header: "White Score", Cell: row => row.original.whitePlayerScore},
            {Header: "Last Move", Cell: row => this.timeAgo.format(row.original.lastUpdateTimestamp)}
        ];
    }

    handleNewGameType(gameType) {
        this.setState(
            {selectedGameType: gameType},
            () => {
                this.retrieveGames(this.state.pagedListState.pageStartOffset, this.state.pagedListState.pageSizeLimit);
                this.retrieveGameCount(this.state.pagedListState.pageStartOffset, this.state.pagedListState.pageSizeLimit);
            }
        );
    }

    render() {
        return (
            <div>
                <div className="mui-divider"></div>
                <h3>{this.getGameListHeader()}</h3>
                <UpdatingSelect
                    label="Filter By Game Type"
                    optionChangeHandler={this.handleNewGameType.bind(this)}
                    options={GameType.all()}
                    allOption={true}
                />
                <ReactTable
                    manual
                    getTrProps={(state, rowInfo) => rowInfo ? this.getRowPropsForGame(rowInfo.original) : {}}
                    columns={this.getGamesTableColumns()}
                    sortable={false}
                    loading={this.state.pagedListState.loading}
                    defaultPageSize={this.state.pagedListState.pageSizeLimit}
                    pageSizeOptions={this.state.pagedListState.pageSizeOptions}
                    pages={this.state.pagedListState.pages}
                    data={this.state.pagedListState.objects}
                    onPageChange={this.handlePageChange.bind(this)}
                    onPageSizeChange={this.handlePageSizeChange.bind(this)}
                />
            </div>
        );
    }
}

GameList.propTypes = {
    gameService: PropTypes.object.isRequired,
    userUuid: PropTypes.string.isRequired
};
