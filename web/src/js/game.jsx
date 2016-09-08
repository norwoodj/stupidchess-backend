import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';
import {Game} from './components/game';


$(() => {
    ReactDOM.render(
        <Game httpService={$} gameUuid="6fd8f576-9bce-4adc-8491-ff2ae3f94072"/>,
        document.getElementById('game-panel')
    );
});
