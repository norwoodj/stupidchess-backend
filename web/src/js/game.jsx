import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';
import {Game} from './components/game';


$(() => {
    ReactDOM.render(
        <Game httpService={$} gameUuid="0fa0f3e7-c7c1-475e-98e8-0e80a66d4367"/>,
        document.getElementById('game-panel')
    );
});
