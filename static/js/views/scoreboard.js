function addCell(row, currentTurn, color, className, text) {
    var cell = row.insertCell(-1);
    cell.className = `${className} ${currentTurn == color ? 'current-turn' : ''}`;
    cell.innerHTML = text;
}

function drawScoreboard(gameState) {
    var scoreboardElement = document.getElementById('scoreboard');
    var scoreboardHeaders = scoreboardElement.getElementsByTagName('thead');
    var scoreboardBodies = scoreboardElement.getElementsByTagName('tbody');

    for (var i = 0; i < scoreboardHeaders.length; ++i) scoreboardElement.removeChild(scoreboardHeaders[i]);
    for (var i = 0; i < scoreboardBodies.length; ++i) scoreboardElement.removeChild(scoreboardBodies[i]);

    var scoreboardHeader = scoreboardElement.createTHead();
    var headerRow = scoreboardHeader.insertRow(-1);
    addCell(headerRow, gameState.currentTurn, 'BLACK', 'score-name-cell', gameState.blackUsername);
    addCell(headerRow, gameState.currentTurn, 'WHITE', 'score-name-cell', gameState.whiteUsername);

    var scoreRow = scoreboardElement.insertRow(-1);
    addCell(scoreRow, gameState.currentTurn, 'BLACK', 'score-score-cell', gameState.blackScore);
    addCell(scoreRow, gameState.currentTurn, 'WHITE', 'score-score-cell', gameState.whiteScore);
}
