import React from 'react';
import Button from 'muicss/lib/react/button';
import Form from 'muicss/lib/react/form';
import Input from 'muicss/lib/react/input';
import Option from 'muicss/lib/react/option';
import Panel from 'muicss/lib/react/panel';
import Select from 'muicss/lib/react/select';
import Container from 'muicss/lib/react/container';

import GameService from '../services/game-service';
import {GameAuthType} from '../constants';
import {toTitleCase} from '../util';


class GameForm extends React.Component {

    constructor() {
        super();

        this.otherPlayer = '';
        this.selectedGameType = null;
        this.selectedGameAuthType = null;
        this.state = {
            gameTypes: [],
            gameAuthTypes: [],
            selectedGameAuthType: null
        };
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
            error => console.log(error)
        );

        this.gameService.getPossibleGameAuthTypes().then(
            gameAuthTypes => this.setState({
                    gameAuthTypes: gameAuthTypes,
                    selectedGameAuthType: gameAuthTypes[0]
            }),
            error => console.log(error)
        );
    }

    handleSubmit(event) {
        event.preventDefault();

        if (this.state.selectedGameAuthType == GameAuthType.TWO_PLAYER && this.otherPlayer.length == 0) {
            return;
        }

        var createGameRequest = {
            type: this.selectedGameType,
            gameAuthType: this.state.selectedGameAuthType
        };

        if (this.state.selectedGameAuthType == GameAuthType.TWO_PLAYER) {
            createGameRequest.otherPlayer = this.otherPlayer;
        }

        this.gameService.createGame(createGameRequest).then(
            response => window.location.replace(`/game.html?gameuuid=${response.gameUuid}`),
            error => console.log(error)
        );
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

    render() {
        return (
            <Container className="game-form-container">
                <Panel>
                    <Form>
                        <legend>Create New Game</legend>
                        <Select onChange={this.updateGameType.bind(this)}>{ this.state.gameTypes.map(
                            gameType => <Option key={gameType} value={gameType} label={toTitleCase(gameType)}/>
                        )}</Select>
                        <Select onChange={this.updateGameAuthType.bind(this)}>{ this.state.gameAuthTypes.map(
                            gameAuthType => <Option key={gameAuthType} value={gameAuthType} label={toTitleCase(gameAuthType)}/>
                        )}</Select>{ this.state.selectedGameAuthType == GameAuthType.TWO_PLAYER
                            ? <Input
                                label="Other Player's name"
                                hint="Other Player's name"
                                required={true}
                                onChange={this.updateOtherPlayer.bind(this)}
                            />
                            : null
                        }
                        <Button className="submit-button" onClick={this.handleSubmit.bind(this)} variant="raised">Submit</Button>
                    </Form>
                </Panel>
            </Container>
        );
    }
}

GameForm.propTypes = {
    httpService: React.PropTypes.func.isRequired
};

export {GameForm};
