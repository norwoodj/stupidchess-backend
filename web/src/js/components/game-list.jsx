import React from "react";
import PropTypes from "prop-types";
import ReactTable from "react-table";
import {UpdatingSelect} from "../components/updating-select"
import GameService from "../services/game-service"
import {Color, GameResult, GameType} from "../constants";
import timeago from "timeago.js";


class GameList extends React.Component {
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
        this.gameService = new GameService(this.props.httpService);
        this.retrieveGames(this.state.offset, this.state.limit);
        this.retrieveGameCount();
    }

    static getClassNameForGameResult(game) {
        if (!game || game.gameResult == null) {
            return "game-active"
        } else if (game.gameResult == GameResult.WIN) {
            return "game-win"
        } else if (game.gameResult == GameResult.LOSS) {
            return "game-loss"
        } else if (game.gameResult == GameResult.TIE) {
            return "game-tie"
        }
    }

    static getUuidLinkElementForGame(game) {
        let className = game.gameResult == null ? "uuid-link" : "uuid-link link";
        return <a className={className} href={`/game?gameUuid=${game.id}`}>{game.id}</a>
    }

    getUserColor(game) {
        if (this.props.userUuid == game.blackPlayerUuid) {
            return Color.BLACK;
        } else {
            return Color.WHITE;
        }
    }

    getOpponentNameElement(game, className) {
        let myColor = this.getUserColor(game);

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
        return <div className={`color-label-${myColor.toLowerCase()}`}>{myColor}</div>;
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
            {Header: "ID", Cell: row => GameList.getUuidLinkElementForGame(row.original)},
            {Header: "Game Type", Cell: row => row.original.type},
            {Header: "User Color", Cell: row => this.getUserColorElement(row.original)},
            {Header: "Opponent", Cell: row => this.getOpponentNameElement(row.original, "")},
            {Header: "Black Score", Cell: row => row.original.blackPlayerScore},
            {Header: "White Score", Cell: row => row.original.whitePlayerScore},
            {Header: "Last Move", Cell: row => this.timeAgo.format(row.original.lastUpdateTimestamp + "Z")}
        ];
    }

    handleNewGameType(gameType) {
        this.setState({selectedGameType: gameType}, () => this.retrieveGames(this.state.offset, this.state.limit));
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
                    getTrProps={(state, rowInfo) => { return {className: rowInfo ? GameList.getClassNameForGameResult(rowInfo.original) : {}}; }}
                    columns={this.getGamesTableColumns()}
                    defaultPageSize={this.state.limit}
                    pageSizeOptions={[5, 10, 15, 25, 50]}
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
    httpService: PropTypes.func.isRequired,
    userUuid: PropTypes.string.isRequired
};

export {GameList};
