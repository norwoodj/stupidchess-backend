import React from "react";
import {GameTypeSelect} from "../components/game-type-select"
import GameService from "../services/game-service"
import {handleUnauthorized} from "../util";
import {Color, GameResult, GameType} from "../constants";


class GameList extends React.Component {
    constructor() {
        super();
        this.gameTypes = ["ALL", ...GameType.all()];

        this.state = {
            selectedGameType: "ALL",
            games: []
        }
    }

    componentDidMount() {
        this.gameService = new GameService(this.props.httpService);
        this.retrieveGames().then(
            games => this.setState({games: games}),
            handleUnauthorized
        );

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
                return <a className={className} href={`/profile.html?playeruuid=${game.whitePlayerUuid}`}>{game.whitePlayerName}</a>;
            } else {
                return <a className={className} href={`/profile.html?playeruuid=${game.blackPlayerUuid}`}>{game.blackPlayerName}</a>;
            }
        } else {
            return (myColor == Color.BLACK) ? game.whitePlayerName : game.blackPlayerName;
        }
    }

    static getClassNameForGameResult(gameResult) {
        if (gameResult == null) {
            return "game-active"
        } else if (gameResult == GameResult.WIN) {
            return "game-win"
        } else if (gameResult == GameResult.LOSS) {
            return "game-loss"
        } else if (gameResult == GameResult.TIE) {
            return "game-tie"
        }
    }

    retrieveGames(gameType) {
        if (gameType == "ALL") {
            return this.doRetrieveGames(null);
        } else {
            return this.doRetrieveGames(gameType);
        }
    }

    getGamesTableDataRow(game, gameIndex) {
        return (
            <tr className={GameList.getClassNameForGameResult(game.gameResult)} key={gameIndex}>{this.getGamesTableData(game).map(
                (data, cellIndex) => <td key={gameIndex * 10 + cellIndex}>{data}</td>
            )}</tr>
        );
    }

    handleNewGameType(gameType) {
        this.setState({
            selectedGameType: gameType
        });

        this.retrieveGames(gameType).then(
            games => this.setState({games: games}),
            handleUnauthorized
        );
    }

    render() {
        return (
            <div>
                <div className="mui-divider"></div>
                <h3>{this.getGameListHeader()}</h3>
                <GameTypeSelect
                    optionChangeHandler={this.handleNewGameType.bind(this)}
                    options={GameType.all()}
                    allOption={true}
                />
                <table className="mui-table mui-table--bordered">
                    <thead>
                    <tr>{this.getGamesTableHeaders().map((header, index) =>
                        <th key={index}>{header}</th>
                    )}</tr>
                    </thead>
                    <tbody>{this.state.games.map((game, gameIndex) => this.getGamesTableDataRow(game, gameIndex))}</tbody>
                </table>
            </div>
        );
    }
}

GameList.propTypes = {
    httpService: React.PropTypes.func.isRequired,
    userUuid: React.PropTypes.string.isRequired
};

export {GameList};
