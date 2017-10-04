import PropTypes from "prop-types";
import {GameList} from "./game-list";


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
}

ActiveGameList.propTypes = {
    httpService: PropTypes.func.isRequired,
    userUuid: PropTypes.string
};

export {ActiveGameList};
