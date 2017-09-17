import React from "react";
import Select from "muicss/lib/react/select";
import Input from "muicss/lib/react/input";
import Option from "muicss/lib/react/option";

import GameService from "../services/game-service";
import {GameAuthType} from "../constants";
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
        this.state.selectedGameAuthType = null;
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
                this.selectedGameType = "STUPID_CHESS";
                this.setState({
                    gameTypes: ["STUPID_CHESS"]
                });
            }
        );

        this.gameService.getPossibleGameAuthTypes().then(
            gameAuthTypes => this.setState({
                    gameAuthTypes: gameAuthTypes,
                    selectedGameAuthType: gameAuthTypes[0]
            }),
            () => {
                this.setState({errors: "Failed to retrieve possible game authentication types from server! Using default"});
                this.selectedGameType = "ONE_PLAYER";
                this.setState({
                    gameTypes: ["ONE_PLAYER", "TWO_PLAYER"]
                });
            }
        );
    }

    errorCheck() {
        if (this.state.selectedGameAuthType == GameAuthType.TWO_PLAYER && this.otherPlayer.length == 0) {
            this.setState({errors: "Other player's name needs to be provided for a 2 player game"});
            return false;
        }

        return true;
    }

    getLegend() {
        return "Create Game";
    }

    getFormRedirectDefault(response) {
        return `/game.html?gameuuid=${response.gameUuid}`;
    }

    renderFormFields() {
        let formFields = [
            <Select key="0" label="Game Type" onChange={this.updateGameType.bind(this)}>{
                this.state.gameTypes.map(
                    gameType => <Option key={gameType} value={gameType} label={toTitleCase(gameType)}/>
                )
            }</Select>,
            <Select key="1" label="Number of Players" onChange={this.updateGameAuthType.bind(this)}>{
                this.state.gameAuthTypes.map(
                    gameAuthType => <Option key={gameAuthType} value={gameAuthType} label={toTitleCase(gameAuthType)}/>
                )
            }</Select>
        ];

        if (this.state.selectedGameAuthType == GameAuthType.TWO_PLAYER) {
            formFields.push(
                <Input
                    key="2"
                    label="Other Player's name"
                    hint="Other Player's name"
                    required={true}
                    onChange={this.updateOtherPlayer.bind(this)}
                />
            );
        }

        console.log(formFields);
        return formFields;
    }

    submitForm() {
        let createGameRequest = {
            type: this.selectedGameType,
            gameAuthType: this.state.selectedGameAuthType
        };
        console.log(createGameRequest);

        if (this.state.selectedGameAuthType == GameAuthType.TWO_PLAYER) {
            createGameRequest.otherPlayer = this.otherPlayer;
        }

        return this.gameService.createGame(createGameRequest);
    }

    updateGameType(event) {
        this.selectedGameType = event.target.value;
    }

    updateGameAuthType(event) {
        this.setState({
            selectedGameAuthType: event.target.value
        });
    }

    updateOtherPlayer(event) {
        this.otherPlayer = event.target.value;
    }
}

GameForm.propTypes = {
    httpService: React.PropTypes.func.isRequired
};

export {GameForm};
