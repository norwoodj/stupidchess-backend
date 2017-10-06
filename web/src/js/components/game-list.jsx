import React from "react";
import PropTypes from "prop-types";
import ReactTable from "react-table";
import UpdatingSelect from "../components/updating-select";

import {Color, GameType} from "../constants";
import {toTitleCase} from "../util";
import timeago from "timeago.js";


export default class GameList extends React.Component {
    constructor() {
        super();
        this.state = {
            selectedGameType: "ALL",
            pages: -1,
            gameCount: -1,
            loading: true,
            games: [],
            offset: 0,
            limit: 5
        };

        this.timeAgo = timeago();
    }

    componentDidMount() {
        this.retrieveGames(this.state.offset, this.state.limit);
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

        this.doRetrieveGameCount(gameType).then((gameCount) => this.setState({
                gameCount: gameCount,
                pages: Math.ceil(gameCount / this.state.limit)
            })
        );
    }

    retrieveGames() {
        let gameType = (this.state.selectedGameType == "ALL") ? null : this.state.selectedGameType;

        this.doRetrieveGames(gameType, this.state.offset, this.state.limit).then((games) => this.setState({
                games: games,
                loading: false
            })
        );
    }

    handlePageChange(page) {
        this.setState({
            offset: page * this.state.limit,
            loading: true
        }, () => this.retrieveGames());
    }

    handlePageSizeChange(pageSize, page) {
        this.setState({
            offset: page * pageSize,
            limit: pageSize,
            pages: Math.ceil(this.state.gameCount / pageSize),
            loading: true
        }, () => this.retrieveGames());
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
                this.retrieveGames(this.state.offset, this.state.limit);
                this.retrieveGameCount(this.state.offset, this.state.limit);
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
                    defaultPageSize={this.state.limit}
                    pageSizeOptions={[5, 10, 15, 25, 50]}
                    sortable={false}
                    data={this.state.games}
                    pages={this.state.pages}
                    loading={this.state.loading}
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
