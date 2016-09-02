import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';
import {Game} from './components/game';


$(() => {
    ReactDOM.render(
        <Game httpService={$} gameUuid="uuid"/>,
        document.getElementById('game-panel')
    );
});
