import React from "react";
import Select from "muicss/lib/react/select";
import Input from "muicss/lib/react/input";
import Option from "muicss/lib/react/option";

import GameService from "../services/game-service";
import {GameType, GameAuthType, GAME_TYPES} from "../constants";
import {toTitleCase} from "../util";
import {AbstractForm} from "./abstract-form";


class GameForm extends AbstractForm {

    constructor() {
        super();

        this.otherPlayer = "";
        this.selectedGameType = null;
        this.selectedGameAuthType = null;

        this.state.gameTypes = [];
        this.state.gameAuthTypes = [];
    }

    componentDidMount() {
        this.gameService = new GameService(this.props.httpService);

        this.gameService.getPossibleGameTypes().then(
            gameTypes => {
                this.selectedGameType = gameTypes[0];
                this.setState({
                    gameTypes: gameTypes
                });
            },
            () => {
                this.setState({errors: "Failed to retrieve possible game types from server! Using default"});
                this.selectedGameType = GameType.STUPID_CHESS;
                this.setState({
                    gameTypes: GAME_TYPES
                });
            }
        );

        this.gameService.getPossibleGameAuthTypes().then(
            gameAuthTypes => {
                this.selectedGameAuthType = gameAuthTypes[0];
                this.setState({
                    gameAuthTypes: gameAuthTypes,
                })
            },
            () => {
                this.setState({errors: "Failed to retrieve possible game authentication types from server! Using default"});
                this.selectedGameType = GameAuthType.ONE_PLAYER;
                this.setState({
                    gameTypes: [GameAuthType.ONE_PLAYER, GameAuthType.TWO_PLAYER]
                });
            }
        );
    }

    errorCheck() {
        if (this.otherPlayer.length == 0) {
            this.setState({errors: "Other player's name is required, and must exist as a user for 2 player games"});
            return false;
        }

        return true;
    }

    getLegend() {
        return "Create Game";
    }

    getFormRedirectDefault(response) {
        console.log(response);
        return `/game.html?gameuuid=${response.gameUuid}`;
    }

    renderFormFields() {
        return [
            <Select key="0" label="Game Type" onChange={this.updateGameType.bind(this)}>{
                this.state.gameTypes.map(
                    gameType => <Option key={gameType} value={gameType} label={toTitleCase(gameType)}/>
                )
            }</Select>,
            <Select key="1" label="Number of Players" onChange={this.updateGameAuthType.bind(this)}>{
                this.state.gameAuthTypes.map(
                    gameAuthType => <Option key={gameAuthType} value={gameAuthType} label={toTitleCase(gameAuthType)}/>
                )
            }</Select>,
            <Input
                key="2"
                label="Other Player's name"
                hint="Other Player's name"
                required={true}
                onChange={this.updateOtherPlayer.bind(this)}
            />
        ];
    }

    submitForm() {
        let createGameRequest = {
            type: this.selectedGameType,
            gameAuthType: this.selectedGameAuthType,
            otherPlayer: this.otherPlayer
        };

        return this.gameService.createGame(createGameRequest);
    }

    updateGameType(event) {
        this.selectedGameType = event.target.value;
    }

    updateGameAuthType(event) {
        this.selectedGameAuthType = event.target.value;
    }

    updateOtherPlayer(event) {
        this.otherPlayer = event.target.value;
    }
}

GameForm.propTypes = {
    httpService: React.PropTypes.func.isRequired
};

export {GameForm};
