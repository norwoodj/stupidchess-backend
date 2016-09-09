import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';
import {Game} from './components/game';
import {getQueryParam} from './util';


$(() => {
    let gameUuid = getQueryParam('gameuuid');

    ReactDOM.render(
        <Game httpService={$} gameUuid={gameUuid}/>,
        document.getElementById('game-panel')
    );
});
