import React from "react";
import PropTypes from "prop-types";
import {isGameInBoardSetupMode, toTitleCase} from "../util";


let SETUP_BOARD_MESSAGE = [
    "Board needs to be set up to start Stupid Chess game. To place a piece, click on a square in the",
    "setup zone (bottom three rows). That square will highlight, then click on the piece you wish to place there"
].join(" ");

let COLOR_MUST_PLACE_PIECE_MESSAGE_FN = (color) => [
    `${toTitleCase(color)} must replace the highlighted pawn with one of the available pieces. Select the piece`,
    "to replace it with"
].join(" ");

let AMBIGUOUS_MOVE_SELECTED_MESSAGE = [
    "There is more than one way to get to the square that you have selected, highlighted are the pieces that you",
    "can capture along the way. Select which piece you would like to capture, or click on the checker to move",
    "a different piece"
].join(" ");

let COLORS_TURN_TO_MOVE_MESSAGE_FN = (color) => [
    `${toTitleCase(color)}'s turn to move. Click on the piece that you would like to move to see available moves.`,
    "Then, to move to a square, click on it. If you would not like to move that piece after all, click on the piece",
    "again"
].join(" ");


class HelpText extends React.Component {

    getHelpText() {
        if (isGameInBoardSetupMode(this.props.gameState)) {
            return SETUP_BOARD_MESSAGE;
        } else if (this.props.gameState.mustPlacePiece()) {
            return COLOR_MUST_PLACE_PIECE_MESSAGE_FN(this.props.gameState.currentTurn);
        } else if (this.props.ambiguousMoveState.isAmbiguousDestinationSelected()) {
            return AMBIGUOUS_MOVE_SELECTED_MESSAGE;
        } else {
            return COLORS_TURN_TO_MOVE_MESSAGE_FN(this.props.gameState.currentTurn);
        }
    }

    render() {
        return <div className="help-text">{this.getHelpText()}</div>;
    }
}

HelpText.propTypes = {
    gameState: PropTypes.object.isRequired,
    ambiguousMoveState: PropTypes.object.isRequired
};

export {HelpText};
