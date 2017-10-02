import React from "react";
import Container from "muicss/lib/react/container";
import Panel from "muicss/lib/react/panel";
import Button from "muicss/lib/react/button";
import GameService from "../services/game-service";

import {ActiveGameList} from "./active-game-list";
import {PlayerRecord} from "./player-record";
import {CompletedGameList} from "./completed-game-list";
import {ErrorElement} from "./error-element";


class Profile extends React.Component {
    constructor() {
        super();
        this.state = {
            playerUuid: null,
            playerName: "",
            games: [],
        }
    }

    componentDidMount() {
        this.gameService = new GameService(this.props.httpService);
    }

    render() {
        return (
            <Container>
                <Panel>
                    <ErrorElement error={this.props.error}/>
                    <h2>{this.props.profileUsername}</h2>

                    <div className="mui-divider"></div>
                    <ActiveGameList httpService={this.props.httpService} userUuid={this.props.profileUserUuid}/>

                    <div className="mui-divider"></div>
                    <CompletedGameList httpService={this.props.httpService} userUuid={this.props.profileUserUuid}/>

                    <div className="mui-divider"></div>
                    <PlayerRecord httpService={this.props.httpService} userUuid={this.props.profileUserUuid}/>

                    <a href="/create-game">
                        <Button className="button" variant="fab">+</Button>
                    </a>
                </Panel>
            </Container>
        );
    }
}

Profile.propTypes = {
    httpService: React.PropTypes.func.isRequired,
    profileUsername: React.PropTypes.string.isRequired,
    profileUserUuid: React.PropTypes.string.isRequired,
    error: React.PropTypes.string
};

export {Profile};
