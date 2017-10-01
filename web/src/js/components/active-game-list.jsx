import React from "react";
import {GameList} from "./game-list";


class ActiveGameList extends GameList {
    getGamesTableHeaders() {
        return [
            "ID",
            "Game Type",
            "User Color",
            "Opponent",
            "Black Score",
            "White Score",
            "Last Move"
        ];
    }

    getGamesTableData(game) {
        return [
            <a className="uuid-link" href={`/game?gameUuid=${game.id}`}>{game.id}</a>,
            game.type,
            this.getUserColor(game),
            this.getOpponentNameElement(game, ""),
            game.blackPlayerScore,
            game.whitePlayerScore,
            game.lastUpdateTimestamp
        ];
    }

    getGameListHeader() {
        return "Active Games";
    }

    doRetrieveGames(gameType) {
        return this.gameService.getActiveGames(gameType);
    }
}

ActiveGameList.propTypes = {
    httpService: React.PropTypes.func.isRequired,
    userUuid: React.PropTypes.string
};

export {ActiveGameList};
