import React from "react";
import PropTypes from "prop-types";
import ReactTable from "react-table";
import RecordService from "../services/record-service";
import {GameType} from "../constants";
import {toTitleCase} from "../util";


class PlayerRecord extends React.Component {
    constructor() {
        super();
        this.state = {
            playerRecords: [],
            loading: true
        };
    }

    componentDidMount() {
        this.recordService = new RecordService(this.props.httpService);
        this.recordService.getUserGameRecords(this.props.userUuid, this.state.selectedGameType).then(
            playerRecords => {
            this.setState({
                playerRecords: this.convertPlayerRecordResponse(playerRecords),
                loading: false
            });
        });
    }

    convertPlayerRecordResponse(playerRecords) {
        return GameType.all().map(gameType => Object.assign({gameType: toTitleCase(gameType)}, playerRecords[gameType]));
    }

    getPlayerRecordColumns() {
        return [
            {Header: "Type", Cell: row => row.original.gameType},
            {Header: "Games", Cell: row => row.original.wins + row.original.losses},
            {Header: "Wins", Cell: row => row.original.wins},
            {Header: "Losses", Cell: row => row.original.losses},
            {Header: "Point Differential", Cell: row => row.original.pointDifferential}
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
                <ReactTable
                    manual
                    defaultPageSize={GameType.all().length}
                    columns={this.getPlayerRecordColumns()}
                    sortable={false}
                    showPagination={false}
                    data={this.state.playerRecords}
                    loading={this.state.loading}
                />
            </div>
        );
    }
}

PlayerRecord.propTypes = {
    httpService: PropTypes.func.isRequired,
    userUuid: PropTypes.string.isRequired
};

export {PlayerRecord};
