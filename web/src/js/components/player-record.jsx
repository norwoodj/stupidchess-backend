import React from "react";
import RecordService from "../services/record-service";
import {handleUnauthorized} from "../util";
import {GameTypeSelect} from "../components/game-type-select";
import {GameType} from "../constants";


class PlayerRecord extends React.Component {
    constructor() {
        super();
        this.state = {
            playerRecords: [],
        };
    }

    componentDidMount() {
        this.recordService = new RecordService(this.props.httpService);
        this.recordService.getUserGameRecords(this.props.playerUuid, this.state.selectedGameType).then(
            playerRecords => this.setState({playerRecords: playerRecords}),
            handleUnauthorized
        );
    }

    getPlayerRecordHeaders() {
        return [
            "Games",
            "Wins",
            "Losses"
        ]
    }

    getPlayerRecordData() {
        return [
            this.state.playerRecords.completedGames,
            this.state.playerRecords.wins,
            this.state.playerRecords.losses
        ];
    }

    handleNewGameType(gameType) {
        this.setState({
            selectedGameType: gameType
        });

        this.recordService.getUserGameRecords(this.props.playerUuid, gameType).then(
            playerRecords => this.setState({playerRecords: playerRecords}),
            handleUnauthorized
        );
    }

    render() {
        return (
            <div>
                <div className="mui-divider"></div>
                <h3>Record Against Other Players</h3>
                <GameTypeSelect
                    optionChangeHandler={this.handleNewGameType.bind(this)}
                    options={GameType.all()}
                    allOption={true}
                />
                <table className="mui-table mui-table--bordered">
                    <thead>
                    <tr>{this.getPlayerRecordHeaders().map((header, index) => <th key={index}>{header}</th>)}</tr>
                    </thead>
                    <tbody>
                    <tr>{this.getPlayerRecordData().map((data, index) => <td key={index}>{data}</td>)}</tr>
                    </tbody>
                </table>
            </div>
        );
    }
}

PlayerRecord.propTypes = {
    httpService: React.PropTypes.func.isRequired,
    playerUuid: React.PropTypes.string.isRequired
};

export {PlayerRecord};
