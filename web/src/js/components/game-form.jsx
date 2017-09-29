import React from "react";
import Input from "muicss/lib/react/input";

import GameService from "../services/game-service";
import {GameType, GameAuthType} from "../constants";
import {AbstractForm} from "./abstract-form";
import {GameTypeSelect} from "./game-type-select";
import {GameAuthTypeSelect} from "./game-auth-type-select";


class GameForm extends AbstractForm {

    constructor() {
        super();

        this.otherPlayer = "";
        this.selectedGameType = GameType.STUPID_CHESS;
        this.selectedGameAuthType = GameAuthType.ONE_PLAYER;
    }

    componentDidMount() {
        this.gameService = new GameService(this.props.httpService);
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
        return `/game.html?gameuuid=${response.game.id}`;
    }

    updateGameType(gameType) {
        this.selectedGameType = gameType;
    }

    updateGameAuthType(gameAuthType) {
        this.selectedGameAuthType = gameAuthType;
    }

    updateOtherPlayer(event) {
        this.otherPlayer = event.target.value;
    }

    submitForm() {
        let createGameRequest = {
            type: this.selectedGameType,
            gameAuthType: this.selectedGameAuthType,
            otherPlayer: this.otherPlayer
        };

        return this.gameService.createGame(createGameRequest);
    }

    renderFormFields() {
        return (
            <div>
                <GameTypeSelect
                    allOption={false}
                    options={GameType.all()}
                    optionChangeHandler={this.updateGameType.bind(this)}
                />
                <GameAuthTypeSelect
                    allOption={false}
                    options={GameAuthType.all()}
                    optionChangeHandler={this.updateGameAuthType.bind(this)}
                />
                <Input
                    label="Other Player's name"
                    hint="Other Player's name"
                    required={true}
                    onChange={this.updateOtherPlayer.bind(this)}
                />
            </div>
        );
    }
}

GameForm.propTypes = {
    httpService: React.PropTypes.func.isRequired
};

export {GameForm};
