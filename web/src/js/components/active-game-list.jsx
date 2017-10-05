import PropTypes from "prop-types";
import {GameList} from "./game-list";
import {isGameInBoardSetupMode} from "../util";


class ActiveGameList extends GameList {
    getGameListHeader() {
        return "Active Games";
    }

    doRetrieveGames(gameType, offset, limit) {
        return this.gameService.getActiveGames(this.props.userUuid, gameType, offset, limit);
    }

    doRetrieveGameCount(gameType) {
        return this.gameService.getActiveGameCount(this.props.userUuid, gameType);
    }

    getRowPropsForGame(game) {
        if (this.getUserColor(game) == game.currentTurn || isGameInBoardSetupMode(game)) {
            return {className: "game-my-turn"};
        }

        return "";
    }
}

ActiveGameList.propTypes = {
    httpService: PropTypes.func.isRequired,
    userUuid: PropTypes.string
};

export {ActiveGameList};
