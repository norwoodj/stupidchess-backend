import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';

import {ScAppBar} from './components/app-bar';
import {SideDrawer} from './components/side-drawer';
import {Footer} from './components/footer';
import {GameForm} from './components/game-form';
import {setupSideDrawerTransition} from './side-drawer-transition';
import {MENU_CATEGORIES, APP_NAME} from './constants';


$(() => {
    ReactDOM.render(
        <div id="react-root">
            <SideDrawer pageName={APP_NAME} menuCategories={MENU_CATEGORIES}/>
            <ScAppBar appName={APP_NAME} httpService={$}/>
            <div id="content-wrapper">
                <div className="mui--appbar-height"></div>
                <GameForm httpService={$}/>
            </div>
            <Footer/>
        </div>,
        document.getElementById('game-form')
    );

    setupSideDrawerTransition();
});
