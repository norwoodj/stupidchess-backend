import React from "react";
import PropTypes from "prop-types";
import Panel from "muicss/lib/react/panel";
import Button from "muicss/lib/react/button";

import ActiveGameList from "./active-game-list";
import PlayerRecord from "./player-record";
import CompletedGameList from "./completed-game-list";
import ErrorElement from "./error-element";

import GameService from "../services/game-service";
import RecordService from "../services/record-service";
import {getErrorMessage} from "../util";


export default class Profile extends React.Component {
    constructor() {
        super();
        this.state = {
            gameService: null,
            recordService: null,
            playerUuid: null,
            playerName: "",
            games: []
        };
    }

    componentDidMount() {
        if (this.props.error) {
            this.setState({error: this.props.error});
        }

        this.setState({
            gameService: new GameService(this.props.httpService, this.handleError.bind(this)),
            recordService: new RecordService(this.props.httpService, this.handleError.bind(this))
        });
    }

    handleError(error) {
        this.setState({error: getErrorMessage(error)});
    }

    render() {
        if (this.state.gameService == null || this.state.recordService == null) {
            return null;
        }

        return (
            <Panel>
                <ErrorElement error={this.state.error}/>
                <h2>{this.props.profileUsername}</h2>

                <div className="mui-divider"></div>
                <ActiveGameList gameService={this.state.gameService} userUuid={this.props.profileUserUuid}/>

                <div className="mui-divider"></div>
                <CompletedGameList gameService={this.state.gameService} userUuid={this.props.profileUserUuid}/>

                <div className="mui-divider"></div>
                <PlayerRecord recordService={this.state.recordService} userUuid={this.props.profileUserUuid}/>

                <a href="/create-game">
                    <Button className="button" variant="fab">+</Button>
                </a>
            </Panel>
        );
    }
}

Profile.propTypes = {
    httpService: PropTypes.func.isRequired,
    profileUsername: PropTypes.string.isRequired,
    profileUserUuid: PropTypes.string.isRequired,
    error: PropTypes.string
};
