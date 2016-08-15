function drawColorSetupSelect(gameState, boardSetupState, changeCallback) {
    var colorSetupSelectElement = document.getElementById('color-setup-select');
    var colorSetupSelectFormElements = colorSetupSelectElement.getElementsByTagName('form');

    for (var i = 0; i < colorSetupSelectFormElements.length; ++i) {
        colorSetupSelectElement.removeChild(colorSetupSelectFormElements[i]);
    }

    if (!gameState.inBoardSetupMode()) {
        return;
    }

    var colorSetupForm = document.createElement('form');
    colorSetupSelectElement.appendChild(colorSetupForm);

    var selectDiv = document.createElement('div');
    selectDiv.className = 'mui-select';
    colorSetupForm.appendChild(selectDiv);

    var colorSetupLabel = document.createElement('label');
    colorSetupLabel.innerHTML = 'Select Color to Setup';
    selectDiv.appendChild(colorSetupLabel);

    var colorSetupSelect = document.createElement('select');
    selectDiv.appendChild(colorSetupSelect);

    gameState.getColorsSettingUp().forEach(color => {
        var colorOption = document.createElement('option');
        colorOption.innerHTML = toTitleCase(color);
        colorSetupSelect.appendChild(colorOption);
    });

    colorSetupSelect.value = toTitleCase(boardSetupState.getCurrentBoardBeingSetUp());
    colorSetupSelect.onchange = e => changeCallback(e.target.selectedOptions[0].innerHTML);
}
