import PropTypes from "prop-types";
import GameList from "./game-list";
import {isGameInBoardSetupMode} from "../util";


export default class ActiveGameList extends GameList {
    getGameListHeader() {
        return "Active Games";
    }

    doRetrieveGames(gameType, offset, limit) {
        return this.props.gameService.getActiveGames(this.props.userUuid, gameType, offset, limit);
    }

    doRetrieveGameCount(gameType) {
        return this.props.gameService.getActiveGameCount(this.props.userUuid, gameType);
    }

    getRowPropsForGame(game) {
        if (this.getUserColor(game) == game.currentTurn || isGameInBoardSetupMode(game)) {
            return {className: "game-my-turn"};
        }

        return "";
    }
}

ActiveGameList.propTypes = {
    gameService: PropTypes.object.isRequired,
    userUuid: PropTypes.string
};
