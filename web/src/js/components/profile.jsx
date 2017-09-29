import React from "react";
import Container from "muicss/lib/react/container";
import Panel from "muicss/lib/react/panel";
import UserService from "../services/user-service";
import GameService from "../services/game-service";
import {ActiveGameList} from "./active-game-list";
import {PlayerRecord} from "./player-record";
import {CompletedGameList} from "./completed-game-list";
import {handleUnauthorized} from "../util";


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
        this.userService = new UserService(this.props.httpService);

        if (this.props.playerUuid == null || this.props.playerUuid == this.props.currentUserUuid) {
            this.setState({
                playerName: this.props.currentUsername,
                playerUuid: this.props.currentUserUuid
            });

            return;
        }

        this.setState({playerUuid: this.props.playerUuid});
        this.getOtherPlayerInfo();
    }

    getOtherPlayerInfo() {
        this.userService.getUserForUuid(this.state.playerUuid).then(
            user => this.setState({playerName: user.username}),
            handleUnauthorized
        )
    }

    getActiveGameListElements() {
        if (this.props.currentUserUuid == this.state.playerUuid) {
            return (
                <div>
                    <div className="mui-divider"></div>
                    <ActiveGameList httpService={this.props.httpService} userUuid={this.state.playerUuid}/>
                </div>
            );
        }

        return null;
    }

    render() {
        return (
            <Container>
                <Panel>
                    <h2>{this.state.playerName}</h2>

                    {this.getActiveGameListElements()}

                    <div className="mui-divider"></div>
                    {this.state.playerUuid != null ?
                        <div>
                            <CompletedGameList
                                httpService={this.props.httpService}
                                userUuid={this.state.playerUuid}
                                gameType={this.state.selectedGameType}
                            />
                            <PlayerRecord httpService={this.props.httpService} playerUuid={this.state.playerUuid}/>
                        </div>
                        : null
                    }
                </Panel>
            </Container>
        );
    }
}

Profile.propTypes = {
    httpService: React.PropTypes.func.isRequired,
    currentUsername: React.PropTypes.string.isRequired,
    currentUserUuid: React.PropTypes.string.isRequired,
    playerUuid: React.PropTypes.string
};

export {Profile};
