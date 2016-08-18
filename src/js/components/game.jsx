import React from 'react';

import Board from './board';
import CaptureGrid from './capture-grid';
import Scoreboard from './scoreboard'
import ColorSetupSelect from './color-setup-select'
import PieceSelectGrid from './piece-select-grid'

import BoardSetupState from '../models/board-setup-state';
import DisplayState from '../models/display-state';
import SquareSelectionState from '../models/square-selection-state';
import GameState from '../models/game-state';

import GameService from '../services/game-service';
import {getMoveObjectForPieceMove, getMoveObjectForPlacePiece} from '../factories/move-factory';


export default class Game extends React.Component {
    constructor() {
        super();
        this.state = {
            gameState: new GameState(),
            boardSetupState: new BoardSetupState(),
            displayState: new DisplayState(),
            squareSelectionState: new SquareSelectionState()
        };
    }

    refresh() {
        this.setState(this.state);
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
            if (gameResponse.lastMove != this.state.gameState.lastMove) {
                this.state.gameState.updateFromApiResponse(gameResponse);
                this.state.squareSelectionState.clear();

                if (this.state.gameState.inBoardSetupMode()) {
                    this.state.boardSetupState.updateFromColorsSettingUp(this.state.gameState.getColorsSettingUp());
                }

                this.refresh();
            }
        })
    }

    handleColorSetupSelect(colorSelected) {
        this.state.boardSetupState.setUpBoard(colorSelected);
        this.state.squareSelectionState.clear();
        this.refresh();
    }

    handleBoardClick(square) {
        if (this.state.gameState.inBoardSetupMode()) {
            this.handleBoardClickInSetupMode(square);
        } else if (this.state.squareSelectionState.anySquareSelected()) {
            this.handleClickWhilePieceSelected(square);
        } else if (this.state.gameState.hasPieceOnSquare(square)) {
            this.handleClickOnPieceSquareNothingSelected(square);
        }
    }

    handleBoardClickInSetupMode(square) {
        if (this.state.gameState.hasPieceOnSquare(square)) {
            return;
        }

        if (this.state.squareSelectionState.isSquareSelected(square)) {
            this.state.squareSelectionState.clear();
        } else if (this.state.boardSetupState.getCurrentBoardBeingSetUp() == 'BLACK' && Game.isInBlackSetupZone(square)) {
            this.state.squareSelectionState.setSelected(square);
        } else if (this.state.boardSetupState.getCurrentBoardBeingSetUp() == 'WHITE' && Game.isInWhiteSetupZone(square)) {
            this.state.squareSelectionState.setSelected(square);
        }

        this.refresh();
    }

    handleClickWhilePieceSelected(square) {
        if (this.state.squareSelectionState.isSquareSelected(square)) {
            this.state.squareSelectionState.clear();
            this.refresh();
        } else if (this.state.squareSelectionState.isSquarePossibleMove(square) || !this.state.squareSelectionState.isSquarePossibleCapture(square)) {
            var movePieceMove = getMoveObjectForPieceMove(square);
            this.gameService.makeMove(this.gameUuid, movePieceMove).then(() => this.retrieveNewGameState());
        }
    }

    handleClickOnPieceSquareNothingSelected(square) {
        var piece = this.state.gameState.getPieceOnSquare(square);
        if (piece.color != this.state.gameState.currentTurn) {
            return;
        }

        this.gameService.getPossibleMoves(this.gameUuid, square).then((possibleMoves) => {
            if (possibleMoves.length > 0) {
                possibleMoves.forEach(possibleMove => {
                    this.state.squareSelectionState.addPossibleMove(possibleMove.move);
                    possibleMove.captures.forEach(possibleCapture => this.state.squareSelectionState.addPossibleCapture(possibleCapture));
                });

                this.state.squareSelectionState.setSelected(square);
                this.refresh();
            }
        });
    }

    handlePlacePieceSelection(piece) {
        if (!this.state.squareSelectionState.anySquareSelected()) {
            return;
        }

        var placeMove = getMoveObjectForPlacePiece(this.state.squareSelectionState.getSelected(), piece);
        this.gameService.makeMove(this.gameUuid, placeMove).then(() => this.retrieveNewGameState());
    }

    static isInBlackSetupZone(square) {
        return square < 30;
    }

    static isInWhiteSetupZone(square) {
        return square > 90;
    }

    render() {
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
