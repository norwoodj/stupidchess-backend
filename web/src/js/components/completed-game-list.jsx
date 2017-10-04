import PropTypes from "prop-types";
import {GameList} from "./game-list";


class CompletedGameList extends GameList {
    getGameListHeader() {
        return "Completed Games";
    }

    doRetrieveGames(gameType, offset, limit) {
        return this.gameService.getCompletedGames(this.props.userUuid, gameType, offset, limit);
    }

    doRetrieveGameCount(gameType) {
        return this.gameService.getCompletedGameCount(this.props.userUuid, gameType);
    }
}

CompletedGameList.propTypes = {
    httpService: PropTypes.func.isRequired,
    userUuid: PropTypes.string.isRequired,
};

export {CompletedGameList};
