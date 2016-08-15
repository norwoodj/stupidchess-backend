var POLLING_INTERVAL = 5000;

function GameController(http, gameUuid) {
    this.gameService = new GameService(http);
    this.gameUuid = gameUuid;
    this.gameState = new GameState();
    this.displayState = new DisplayState();
    this.boardSetupState = new BoardSetupState();
    this.squareSelectionState = new SquareSelectionState();
}

GameController.prototype = {
    start: function () {
        this.pollGameState();
    },

    pollGameState: function () {
        this.retrieveNewGameState();
        //setTimeout(() => this.pollGameState(), 5000);
    },

    retrieveNewGameState: function () {
        this.gameService.getGameByUuid(this.gameUuid).then((gameResponse) => {
            if (this.gameState == null || gameResponse.lastMove != this.gameState.lastMove) {
                this.gameState.updateFromApiResponse(gameResponse);
                this.squareSelectionState.clear();
                this.boardSetupState.reset();

                if (this.gameState.inBoardSetupMode()) {
                    this.boardSetupState.setUpBoard(this.gameState.getColorsSettingUp()[0])
                }

                this.draw();
            }
        })
    },

    handleColorSetupSelect: function (colorSelected) {
        this.boardSetupState.setUpBoard(colorSelected.toUpperCase());
        this.draw();
    },

    handleBoardClick: function (square) {
        if (this.gameState.inBoardSetupMode()) {
            this.handleBoardClickInSetupMode(square);
        } else if (this.squareSelectionState.anySquareSelected()) {
            this.handleClickWhilePieceSelected(square);
        } else if (this.gameState.hasPieceOnSquare(square)) {
            this.handleClickOnPieceSquareNothingSelected(square);
        }
    },

    handleBoardClickInSetupMode: function (square) {
        if (this.gameState.hasPieceOnSquare(square)) {
            return;
        }

        if (this.squareSelectionState.isSquareSelected(square)) {
            this.squareSelectionState.clear();
            this.draw();
            return;
        }

        if (this.boardSetupState.getCurrentBoardBeingSetUp() == 'BLACK' && this.isInBlackSetupZone(square)) {
            this.squareSelectionState.setSelected(square);
            this.draw();
        } else if (this.boardSetupState.getCurrentBoardBeingSetUp() == 'WHITE' && this.isInWhiteSetupZone(square)) {
            this.squareSelectionState.setSelected(square);
            this.draw();
        }
    },

    handleClickWhilePieceSelected: function (square) {
        if (this.squareSelectionState.isSquareSelected(square)) {
            this.squareSelectionState.clear();
            this.draw();
        } else if (this.squareSelectionState.isSquarePossibleMove(square) || !this.squareSelectionState.isSquarePossibleCapture(square)) {
            var movePieceMove = getMoveObjectForPieceMove(square);
            this.gameService.makeMove(this.gameUuid, movePieceMove).then(() => this.retrieveNewGameState());
        }
    },

    handleClickOnPieceSquareNothingSelected: function (square) {
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
                this.draw();
            }
        });
    },

    handlePlacePieceSelection: function (piece) {
        if (!this.squareSelectionState.anySquareSelected()) {
            return;
        }

        var placeMove = getMoveObjectForPlacePiece(this.squareSelectionState.getSelected(), piece);
        this.gameService.makeMove(this.gameUuid, placeMove).then(() => this.retrieveNewGameState());
    },

    isInBlackSetupZone: (square) => {
        return square < 30;
    },

    isInWhiteSetupZone: (square) => {
        return square > 90;
    },

    draw: function () {
        drawScoreboard(this.gameState);
        drawCaptures(this.gameState);
        drawBoard(this.gameState, this.squareSelectionState, this.displayState, this.boardSetupState, square => this.handleBoardClick(square));
        drawPieceSelections(this.gameState, this.boardSetupState, piece => this.handlePlacePieceSelection(piece));
        drawColorSetupSelect(this.gameState, this.boardSetupState, color => this.handleColorSetupSelect(color));
    }
};
