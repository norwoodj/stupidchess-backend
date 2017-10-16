import PropTypes from "prop-types";
import GameList from "./game-list";


export default class CompletedGameList extends GameList {
    getGameListHeader() {
        return "Completed Games";
    }

    doRetrieveGames(gameType, offset, limit) {
        return this.props.gameService.getCompletedGames(this.props.userUuid, gameType, offset, limit);
    }

    doRetrieveGameCount(gameType) {
        return this.props.gameService.getCompletedGameCount(this.props.userUuid, gameType);
    }

    getUuidLinkClassName() {
        return "uuid-link link";
    }

    getOtherPlayerLinkClassName() {
        return "link";
    }

    getRowPropsForGame(game) {
        return {className: `game-${game.gameResult.toLowerCase()}`};
    }
}

CompletedGameList.propTypes = {
    gameService: PropTypes.object.isRequired,
    userUuid: PropTypes.string.isRequired,
};
