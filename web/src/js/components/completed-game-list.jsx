import React from "react";
import {GameList} from "./game-list";


class CompletedGameList extends GameList {
    getGamesTableHeaders() {
        return [
            "ID",
            "Game Type",
            "User Color",
            "Opponent",
            "Black Score",
            "White Score",
            "Result"
        ];
    }

    getGamesTableData(game) {
        return [
            <a className="uuid-link link" href={`/game.html?gameuuid=${game.id}`}>{game.id}</a>,
            game.type,
            <div className={`color-label-${this.getUserColor(game).toLowerCase()}`}>{this.getUserColor(game)}</div>,
            this.getOpponentNameElement(game, "link"),
            game.blackPlayerScore,
            game.whitePlayerScore,
            <div className={CompletedGameList.getClassNameForGameResult(game.gameResult)}>{game.gameResult}</div>
        ];
    }

    getGameListHeader() {
        return "Completed Games";
    }

    doRetrieveGames(gameType) {
        return this.gameService.getCompletedGames(this.props.userUuid, gameType);
    }
}

CompletedGameList.propTypes = {
    httpService: React.PropTypes.func.isRequired,
    userUuid: React.PropTypes.string.isRequired,
};

export {CompletedGameList};
