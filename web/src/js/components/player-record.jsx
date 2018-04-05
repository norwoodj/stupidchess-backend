import React from "react";
import PropTypes from "prop-types";
import ReactTable from "react-table";
import Checkbox from "muicss/lib/react/checkbox";
import {GameType} from "../constants";
import {toTitleCase} from "../util";


export default class PlayerRecord extends React.Component {
    constructor() {
        super();
        this.state = {
            includeOnePlayerGames: false,
            playerRecords: [],
            loading: true
        };
    }

    componentDidMount() {
        this.loadRecords();
    }

    loadRecords() {
        this.props.recordService.getUserGameRecords(this.props.userUuid, this.state.selectedGameType, this.state.includeOnePlayerGames).then(
            playerRecords => this.setState({
                playerRecords: this.convertPlayerRecordResponse(playerRecords),
                loading: false
            })
        );
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

    toggleIncludeOnePlayerGames(evt) {
        this.setState(
            {includeOnePlayerGames: evt.target.checked},
            () => this.loadRecords()
        );
    }

    render() {
        if (this.state.playerRecords == null) {
            return null;
        }

        return (
            <div>
                <div className="mui-divider"></div>
                <h3>Record Against Other Players</h3>
                <Checkbox
                    label="Include One Player Games"
                    checked={this.state.includeOnePlayerGames}
                    onChange={this.toggleIncludeOnePlayerGames.bind(this)}
                />
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
    recordService: PropTypes.object.isRequired,
    userUuid: PropTypes.string.isRequired
};
