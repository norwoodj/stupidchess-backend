import React from 'react';

import {Board} from './board';
import {CaptureGrid} from './capture-grid';
import {Scoreboard} from './scoreboard'
import {ColorSetupSelect} from './color-setup-select'
import {PieceSelectGrid} from './piece-select-grid'

import BoardSetupState from '../models/board-setup-state';
import DisplayState from '../models/display-state';
import SquareSelectionState from '../models/square-selection-state';
import GameState from '../models/game-state';

import GameService from '../services/game-service';
import {getMoveObjectForPieceMove, getMoveObjectForPlacePiece} from '../factories/move-factory';


class Game extends React.Component {
    constructor() {
        super();
        this.gameState = new GameState();
        this.boardSetupState = new BoardSetupState();
        this.displayState = new DisplayState();
        this.squareSelectionState = new SquareSelectionState();

        this.state = {
            gameState: this.gameState,
            boardSetupState: this.boardSetupState,
            displayState: this.displayState,
            squareSelectionState: this.squareSelectionState,
        };
    }

    componentDidMount() {
        this.gameService = new GameService(this.props.httpService);
        this.gameUuid = this.props.gameUuid;
        this.start();
    }

    start() {
        this.pollGameState();
    }

    pollGameState() {
        this.retrieveNewGameState();
        //setTimeout(() => this.pollGameState(), 5000);
    }

    retrieveNewGameState() {
        this.gameService.getGameByUuid(this.gameUuid).then((gameResponse) => {
            console.log(gameResponse);
            if (gameResponse.lastMove != this.gameState.lastMove) {
                this.gameState.updateFromApiResponse(gameResponse);
                this.squareSelectionState.clear();

                if (this.gameState.inBoardSetupMode()) {
                    this.boardSetupState.updateFromColorsSettingUp(this.gameState.getColorsSettingUp());
                }

                this.setState({
                    gameState: this.gameState,
                    boardSetupState: this.boardSetupState,
                    displayState: this.displayState,
                    squareSelectionState: this.squareSelectionState
                })
            }
        }, (error) => console.log(error));
    }

    handleColorSetupSelect(colorSelected) {
        this.boardSetupState.setUpBoard(colorSelected);
        this.squareSelectionState.clear();
        this.setState({
            squareSelectionState: this.squareSelectionState,
            boardSetupState: this.boardSetupState,
        });
    }

    handleBoardClick(square) {
        if (this.gameState.inBoardSetupMode()) {
            this.handleBoardClickInSetupMode(square);
        } else if (this.squareSelectionState.anySquareSelected()) {
            this.handleClickWhilePieceSelected(square);
        } else if (this.gameState.hasPieceOnSquare(square)) {
            this.handleClickOnPieceSquareNothingSelected(square);
        }
    }

    handleBoardClickInSetupMode(square) {
        if (this.gameState.hasPieceOnSquare(square)) {
            return;
        }

        if (this.squareSelectionState.isSquareSelected(square)) {
            this.squareSelectionState.clear();
        } else if (this.gameState.squareNeedsPiecePlaced(square)) {
            this.squareSelectionState.setSelected(square);
        }

        this.setState({squareSelectionState: this.squareSelectionState});
    }

    handleClickWhilePieceSelected(square) {
        if (this.squareSelectionState.isSquareSelected(square)) {
            this.squareSelectionState.clear();
            this.setState({squareSelectionState: this.squareSelectionState})
        } else if (this.squareSelectionState.isSquarePossibleMove(square) || !this.squareSelectionState.isSquarePossibleCapture(square)) {
            var movePieceMove = getMoveObjectForPieceMove(square);
            this.gameService.makeMove(this.gameUuid, movePieceMove).then(() => this.retrieveNewGameState());
        }
    }

    handleClickOnPieceSquareNothingSelected(square) {
        var piece = this.gameState.getPieceOnSquare(square);
        if (piece.color != this.gameState.currentTurn) {
            return;
        }

        this.gameService.getPossibleMoves(this.gameUuid, square).then((possibleMoves) => {
            if (possibleMoves.length > 0) {
                possibleMoves.forEach(possibleMove => {
                    this.squareSelectionState.addPossibleMove(possibleMove.move);
                    possibleMove.captures.forEach(possibleCapture => this.squareSelectionState.addPossibleCapture(possibleCapture));
                });

                this.squareSelectionState.setSelected(square);
                this.setState({squareSelectionState: this.squareSelectionState})
            }
        });
    }

    handlePlacePieceSelection(piece) {
        if (!this.squareSelectionState.anySquareSelected()) {
            return;
        }

        var placeMove = getMoveObjectForPlacePiece(this.squareSelectionState.getSelected(), piece);
        this.gameService.makeMove(this.gameUuid, placeMove).then(() => this.retrieveNewGameState());
    }

    render() {
        console.log('Game');
        return (
            <div>
                <div className="row">
                    <Scoreboard gameState={this.state.gameState}/>
                </div>
                <div className="row">
                    <div id="board-block" className="content-block mui-col-lg-8 mui-col-md-12">
                        <Board clickHandler={this.handleBoardClick.bind(this)} {...this.state}/>
                    </div>
                    <div className="content-block mui-col-lg-4 mui-col-md-12">
                        <div className="row">
                            <div className="content-block mui-col-lg-12 mui-col-sm-6">
                                <CaptureGrid gameState={this.state.gameState} captureColor="WHITE"/>
                            </div>
                            <div className="content-block mui-col-lg-12 mui-col-sm-6">
                                <CaptureGrid gameState={this.state.gameState} captureColor="BLACK"/>
                            </div>
                        </div>
                        <div className="row">
                            <div className="content-block mui-col-lg-12 mui-col-sm-6">
                                <PieceSelectGrid
                                    gameState={this.state.gameState}
                                    boardSetupState={this.state.boardSetupState}
                                    pieceSelectionCallback={this.handlePlacePieceSelection.bind(this)}
                                />
                            </div>
                        </div>
                        <div className="row">
                            <div id="color-setup-select" className="content-block mui-col-lg-12 mui-col-sm-6">
                                <ColorSetupSelect
                                    gameState={this.state.gameState}
                                    boardSetupState={this.state.boardSetupState}
                                    colorChangeHandler={this.handleColorSetupSelect.bind(this)}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

Game.propTypes = {
    httpService: React.PropTypes.func.isRequired,
    gameUuid: React.PropTypes.string.isRequired
};

export {Game};
