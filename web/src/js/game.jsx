import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';
import {Game} from './components/game';


$(() => {
    ReactDOM.render(
        <Game httpService={$} gameUuid="088260bf-c2d4-4a7c-b58d-c0a5eea0fe5a"/>,
        document.getElementById('game-panel')
    );
});
