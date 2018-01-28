import React from "react";
import PropTypes from "prop-types";
import Container from "muicss/lib/react/container";

import Board from "./board";
import CaptureGrid from "./capture-grid";
import Scoreboard from "./scoreboard";
import ColorSetupSelect from "./color-setup-select";
import MoveList from "./move-list";
import UpdatingSelect from "./updating-select";
import PieceSelectGrid from "./piece-select-grid";
import ErrorElement from "./error-element";

import BoardSetupState from "../models/board-setup-state";
import SquareSelectionState from "../models/square-selection-state";
import GameState from "../models/game-state";
import AmbiguousMoveState from "../models/ambiguous-move-state";
import PagedListState from "../models/paged-list-state";
import {DISPLAY_STATES_BY_NAME, DISPLAY_STATES_OPTIONS, DefaultDisplayState} from "../models/display-states";

import GameService from "../services/game-service";
import {getMoveObjectForPieceMove, getMoveObjectForPlacePiece, getMoveObjectForReplacePiece} from "../factories/move-factory";
import {getErrorMessage} from "../util";


export default class Game extends React.Component {
    constructor() {
        super();
        this.gameState = new GameState();
        this.boardSetupState = new BoardSetupState();
        this.displayState = new DefaultDisplayState();
        this.squareSelectionState = new SquareSelectionState();
        this.ambiguousMoveState = new AmbiguousMoveState();
        this.pagedListState = new PagedListState();

        this.state = {
            gameService: null,
            gameState: this.gameState,
            boardSetupState: this.boardSetupState,
            displayState: this.displayState,
            squareSelectionState: this.squareSelectionState,
            ambiguousMoveState: this.ambiguousMoveState,
            pagedListState: this.pagedListState,
            error: null
        };
    }

    componentDidMount() {
        if (this.props.error) {
            this.setState({
                error: this.props.error,
                gameService: new GameService(this.props.httpService, this.handleError.bind(this))
            });

            return;
        }

        this.gameUuid = this.props.gameUuid;
        this.setState(
            {gameService: new GameService(this.props.httpService, this.handleError.bind(this))},
            () => this.start()
        );
    }

    handleError(error) {
        this.setState({error: getErrorMessage(error)});
    }

    start() {
        this.retrieveNewGameState();
    }

    retrieveMoveList() {
        this.state.gameService.getMovesForGame(
            this.gameUuid,
            this.state.pagedListState.pageStartOffset,
            this.state.pagedListState.pageSizeLimit
        ).then(moves => {
            this.pagedListState.updateForObjects(moves);
            this.setState(this.pagedListState);
        });
    }

    retrieveMoveCount() {
        this.state.gameService.getMoveCountForGame(this.gameUuid).then(moveCount => {
            this.pagedListState.updateForObjectCount(moveCount);
            this.setState(this.pagedListState);
        });
    }

    handlePageChange(page) {
        this.pagedListState.handlePageChange(page);
        this.setState(this.pagedListState, () => this.retrieveMoveList());
    }

    handlePageSizeChange(pageSize, page) {
        this.pagedListState.handlePageSizeChange(pageSize, page);
        this.setState(this.pagedListState, () => this.retrieveMoveList());
    }

    retrieveNewGameState() {
        this.state.gameService.getGameByUuid(this.gameUuid).then(
            (gameResponse) => {
                if (gameResponse.lastMove != this.gameState.lastMove) {
                    this.retrieveMoveCount();
                    this.retrieveMoveList();

                    this.gameState.updateFromApiResponse(gameResponse);
                    this.squareSelectionState.clear();
                    this.ambiguousMoveState.clear();

                    if (this.gameState.singleSquareToBePlaced()) {
                        for (let square of this.gameState.squaresToBePlaced) {
                            this.squareSelectionState.setSelected(square);
                        }
                    }

                    if (this.gameState.inBoardSetupMode()) {
                        this.boardSetupState.updateFromColorsSettingUp(this.gameState.getColorsSettingUp(this.props.userUuid));
                    }

                    this.setState({
                        gameState: this.gameState,
                        boardSetupState: this.boardSetupState,
                        displayState: this.displayState,
                        squareSelectionState: this.squareSelectionState,
                        ambiguousMoveState: this.ambiguousMoveState
                    });
                }

                setTimeout(() => this.retrieveNewGameState(), 5000);
            }
        );
    }

    handleColorSetupSelect(colorSelected) {
        this.boardSetupState.setUpBoard(colorSelected);
        this.squareSelectionState.clear();
        this.setState({
            squareSelectionState: this.squareSelectionState,
            boardSetupState: this.boardSetupState
        });
    }

    handleBoardClick(square) {
        if (square == null) {
            return;
        }

        if (this.gameState.singleSquareToBePlaced()) {
            return;
        }

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
            this.ambiguousMoveState.clear();
        } else if (this.gameState.squareNeedsPiecePlaced(square)) {
            this.squareSelectionState.setSelected(square);
        }

        this.setState({squareSelectionState: this.squareSelectionState});
    }

    shouldHandleAsDisambiguatingCaptureSelection(square) {
        return (
            this.ambiguousMoveState.isAmbiguousDestinationSelected() &&
            this.ambiguousMoveState.isDisambiguatingCaptureForSelectedSquare(square)
        );
    }

    shouldDeactivateDisambiguatingCaptureSelection(square) {
        return (
            this.ambiguousMoveState.isAmbiguousDestinationSelected() &&
            this.ambiguousMoveState.getSelectedAmbiguousDestination() == square
        );
    }

    handleClickWhilePieceSelected(square) {
        if (this.squareSelectionState.isSquareSelected(square)) {
            this.handleClickOnSelectedSquare();
        } else if (this.shouldDeactivateDisambiguatingCaptureSelection(square)) {
            this.ambiguousMoveState.selectAmbiguousDestination(null);
            this.setState({ambiguousMoveState: this.ambiguousMoveState});
        } else if (this.shouldHandleAsDisambiguatingCaptureSelection(square)) {
            this.handleClickAmbiguousDestinationSelected(square);
        } else if (this.squareSelectionState.isSquarePossibleMove(square)) {
            this.handleClickOnPossibleMoveSquare(square);
        } else if (this.gameState.hasPieceOnSquare(square)) {
            this.squareSelectionState.clear();
            this.ambiguousMoveState.clear();
            this.handleClickOnPieceSquareNothingSelected(square);
        }
    }

    handleClickOnSelectedSquare() {
        this.squareSelectionState.clear();
        this.ambiguousMoveState.clear();
        this.setState({squareSelectionState: this.squareSelectionState});
    }

    handleClickAmbiguousDestinationSelected(square) {
        let movePieceMove = getMoveObjectForPieceMove(
            this.squareSelectionState.getSelected(),
            this.ambiguousMoveState.getSelectedAmbiguousDestination(),
            square
        );

        this.state.gameService.makeMove(this.gameUuid, movePieceMove).then(() => this.retrieveNewGameState());
    }

    handleClickOnPossibleMoveSquare(square) {
        if (this.ambiguousMoveState.isAmbiguousDestination(square)) {
            this.ambiguousMoveState.selectAmbiguousDestination(square);
            this.setState({ambiguousMoveState: this.ambiguousMoveState});
        } else {
            let movePieceMove = getMoveObjectForPieceMove(this.squareSelectionState.getSelected(), square);
            this.state.gameService.makeMove(this.gameUuid, movePieceMove).then(() => this.retrieveNewGameState());
        }
    }

    handleClickOnPieceSquareNothingSelected(square) {
        let piece = this.gameState.getPieceOnSquare(square);

        if (piece.color != this.gameState.currentTurn) {
            return;
        }

        this.state.gameService.getPossibleMoves(this.gameUuid, square).then(
            (possibleMoveResponse) => {
                possibleMoveResponse.possibleMoves.forEach(possibleMove => {
                    this.squareSelectionState.addPossibleMove(possibleMove.destinationSquare);

                    if (possibleMove.hasOwnProperty("captures")) {
                        possibleMove.captures.forEach(possibleCapture => {
                            this.squareSelectionState.addPossibleCapture(possibleCapture.square);
                        });
                    }
                });

                possibleMoveResponse.ambiguousMoves.forEach(ambiguousMove => {
                    this.ambiguousMoveState.addAmbiguousMove(
                        ambiguousMove.destinationSquare,
                        ambiguousMove.disambiguatingCaptures
                    );
                });

                this.squareSelectionState.setSelected(square);
                this.setState({squareSelectionState: this.squareSelectionState});
            }
        );
    }

    handlePlacePieceSelection(piece) {
        if (!this.squareSelectionState.anySquareSelected()) {
            return;
        } else if (!this.gameState.isMyTurn(this.props.userUuid)) {
            return;
        }

        let move = this.gameState.hasPieceOnSquare(this.squareSelectionState.getSelected())
            ? getMoveObjectForReplacePiece(this.squareSelectionState.getSelected(), piece)
            : getMoveObjectForPlacePiece(this.squareSelectionState.getSelected(), piece);

        this.state.gameService.makeMove(this.gameUuid, move).then(() => this.retrieveNewGameState());
    }

    handleDisplayStateChange(displayStateName) {
        let displayStateClass = DISPLAY_STATES_BY_NAME.get(displayStateName);
        this.displayState = new displayStateClass();
        this.setState({displayState: this.displayState});
    }

    render() {
        if (this.state.gameService == null) {
            return null;
        }

        return (
            <Container className="game-panel" style={this.displayState.getGamePanelStyle()} fluid={true}>
                <ErrorElement error={this.state.error}/>

                <div className="row">
                    <Scoreboard gameState={this.state.gameState}/>
                </div>

                <div className="row">
                    <Board clickHandler={this.handleBoardClick.bind(this)} {...this.state}/>
                    <div className="content-block mui-col-md-4 mui-col-sm-12">
                        <Container>
                            <CaptureGrid
                                color={this.displayState.getCaptureGridColor()}
                                gameState={this.state.gameState}
                                captureColor="WHITE"
                            />
                            <CaptureGrid
                                color={this.displayState.getCaptureGridColor()}
                                gameState={this.state.gameState}
                                captureColor="BLACK"
                            />
                        </Container>
                        <PieceSelectGrid
                            color={this.displayState.getPieceSelectGridColor()}
                            gameState={this.state.gameState}
                            boardSetupState={this.state.boardSetupState}
                            pieceSelectionCallback={this.handlePlacePieceSelection.bind(this)}
                        />
                        <ColorSetupSelect
                            gameState={this.state.gameState}
                            boardSetupState={this.state.boardSetupState}
                            colorChangeHandler={this.handleColorSetupSelect.bind(this)}
                            colorsSettingUp={this.state.gameState.getColorsSettingUp(this.props.userUuid)}
                        />
                        <div className="content-block game-page-select">
                            <UpdatingSelect
                                label="Change Theme"
                                options={DISPLAY_STATES_OPTIONS}
                                optionChangeHandler={this.handleDisplayStateChange.bind(this)}
                            />
                        </div>
                        <MoveList
                            pagedListState={this.state.pagedListState}
                            handlePageChangeFn={this.handlePageChange.bind(this)}
                            handlePageSizeChangeFn={this.handlePageSizeChange.bind(this)}
                        />
                    </div>
                </div>
            </Container>
        );
    }
}

Game.propTypes = {
    httpService: PropTypes.func.isRequired,
    gameUuid: PropTypes.string.isRequired,
    userUuid: PropTypes.string.isRequired,
    error: PropTypes.string
};
