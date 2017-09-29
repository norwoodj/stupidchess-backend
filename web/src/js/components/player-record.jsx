import React from "react";
import RecordService from "../services/record-service";
import {handleUnauthorized} from "../util";
import {GameType} from "../constants";


class PlayerRecord extends React.Component {
    constructor() {
        super();
        this.state = {
            playerRecords: null,
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
            "Type",
            "Games",
            "Wins",
            "Losses",
            "Point Differential"
        ]
    }

    getPlayerRecordDataForGameType(gameType) {
        console.log(gameType);
        console.log(this.state.playerRecords);
        let recordsForGameType = this.state.playerRecords[gameType];

        return [
            gameType,
            recordsForGameType.wins + recordsForGameType.losses,
            recordsForGameType.wins,
            recordsForGameType.losses,
            recordsForGameType.pointDifferential
        ];
    }

    render() {
        if (this.state.playerRecords == null) {
            return null;
        }

        return (
            <div>
                <div className="mui-divider"></div>
                <h3>Record Against Other Players</h3>
                <table className="mui-table mui-table--bordered">
                    <thead>
                    <tr>{this.getPlayerRecordHeaders().map((header, index) => <th key={index}>{header}</th>)}</tr>
                    </thead>
                    <tbody>{GameType.all().map((gameType, rowIndex) =>
                        <tr key={rowIndex}>{this.getPlayerRecordDataForGameType(gameType).map((data, index) => <td key={index}>{data}</td>)}</tr>
                    )}</tbody>
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
