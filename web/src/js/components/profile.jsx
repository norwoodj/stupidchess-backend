import React from "react";
import Container from "muicss/lib/react/container";
import Panel from "muicss/lib/react/panel";
import UserService from "../services/user-service";
import GameService from "../services/game-service";
import RecordService from "../services/record-service";
import {handleUnauthorized} from "../util";
import {Color} from "../constants";



class Profile extends React.Component {
    constructor() {
        super();

        this.state = {
            games: [],
            user: {},
            userRecords: []
        }
    }

    componentDidMount() {
        this.gameService = new GameService(this.props.httpService);
        this.userService = new UserService(this.props.httpService);
        this.recordService = new RecordService(this.props.httpService);

        this.gameService.getGames().then(
            games => this.setState({games: games}),
            handleUnauthorized
        );

        this.userService.getCurrentUser().then(
            user => {
                this.setState({user: user});
                this.recordService.getUserGameRecords(user.id).then(
                    userRecords => this.setState({userRecords: userRecords}),
                    handleUnauthorized
                );
            },
            handleUnauthorized
        );

    }

    getMyColor(game) {
        if (this.state.user.username == game.blackPlayerName) {
            return Color.BLACK;
        } else {
            return Color.WHITE;
        }
    }

    getOpponentName(game) {
        if (this.getMyColor(game) == Color.BLACK) {
            return game.whitePlayerName;
        } else {
            return game.blackPlayerName;
        }
    }

    getGamesTableHeaders() {
        return [
            "Game Type",
            "Opponent",
            "Black Score",
            "White Score",
            "Your Color",
            "Link"
        ];
    }

    getGamesTableData(game) {
        return [
            game.type,
            this.getOpponentName(game),
            game.blackPlayerScore,
            game.whitePlayerScore,
            this.getMyColor(game),
            <a href={`/game.html?gameuuid=${game["_id"]}`}>Continue</a>
        ];
    }

    getRecordMetricsHeaders() {
        return [
            "Wins",
            "Losses",
            "Point Differential"
        ]
    }

    getRecordMetricsData() {
        return [
            this.state.userRecords.wins,
            this.state.userRecords.losses,
            this.state.userRecords.point_differential
        ];
    }

    render() {
        return (
            <Container>
                <Panel>
                    <h2>{this.state.user.username}</h2>
                    <div className="mui-divider"></div>

                    <h3>Games In Progress</h3>
                    <table className="mui-table mui-table--bordered">
                        <thead><tr>{this.getGamesTableHeaders().map(header => <th>{header}</th>)}</tr></thead>
                        <tbody>{this.state.games.map(g =>
                            <tr>{this.getGamesTableData(g).map(data => <td>{data}</td>)}</tr>
                        )}</tbody>
                    </table>

                    <div className="mui-divider"></div>
                    <h3>Stupidchess Record Against Other Players</h3>
                    <table className="mui-table mui-table--bordered">
                        <thead><tr>{this.getRecordMetricsHeaders().map(header => <th>{header}</th>)}</tr></thead>
                        <tbody><tr>{this.getRecordMetricsData().map(data => <td>{data}</td>)}</tr></tbody>
                    </table>
                </Panel>
            </Container>
        );
    }
}

Profile.propTypes = {
    httpService: React.PropTypes.func.isRequired,
};

export {Profile};
