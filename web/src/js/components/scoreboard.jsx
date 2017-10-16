import React from "react";
import PropTypes from "prop-types";
import {Color} from "../constants";


export default class Scoreboard extends React.Component {

    getScoreCellClass(color, defaultClass) {
        return `${defaultClass} ${color == this.props.gameState.currentTurn ? "current-turn" : ""}`;
    }

    render() {
        return (
            <table id="scoreboard" className="scoreboard-table">
                <thead>
                <tr>
                    <td className={this.getScoreCellClass(Color.BLACK, "score-name-cell")}>
                        {this.props.gameState.blackPlayerName}
                    </td>
                    <td className={this.getScoreCellClass(Color.WHITE, "score-name-cell")}>
                        {this.props.gameState.whitePlayerName}
                    </td>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td className={this.getScoreCellClass(Color.BLACK, "score-score-cell")}>
                        {this.props.gameState.blackPlayerScore}
                    </td>
                    <td className={this.getScoreCellClass(Color.WHITE, "score-score-cell")}>
                        {this.props.gameState.whitePlayerScore}
                    </td>
                </tr>
                </tbody>
            </table>
        );
    }
}

Scoreboard.propTypes = {
    gameState: PropTypes.object.isRequired
};
