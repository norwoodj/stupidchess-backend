import React from 'react';

export default class Scoreboard extends React.Component {

    getScoreCellClass(color, defaultClass) {
        return `${defaultClass} ${color == this.props.gameState.currentTurn ? 'current-turn' : ''}`;
    }

    render() {
        return (
            <table id="scoreboard">
                <thead>
                    <tr>
                        <td className={this.getScoreCellClass('BLACK', 'score-name-cell')}>
                            {this.props.gameState.blackUsername}
                        </td>
                        <td className={this.getScoreCellClass('WHITE', 'score-name-cell')}>
                            {this.props.gameState.whiteUsername}
                        </td>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td className={this.getScoreCellClass('BLACK', 'score-score-cell')}>
                            {this.props.gameState.blackScore}
                        </td>
                        <td className={this.getScoreCellClass('WHITE', 'score-score-cell')}>
                            {this.props.gameState.whiteScore}
                        </td>
                    </tr>
                </tbody>
            </table>
        );
    }
}

Scoreboard.propTypes = {
    gameState: React.PropTypes.object.isRequired
};
