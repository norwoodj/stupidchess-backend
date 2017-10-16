import $ from "jquery";
import React from "react";
import ReactDOM from "react-dom";

import ScAppBar from "./components/app-bar";
import SideDrawer from "./components/side-drawer";
import Footer from "./components/footer";
import Game from "./components/game";

import {setupSideDrawerTransition} from "./side-drawer-transition";
import {MENU_CATEGORIES, APP_NAME} from "./constants";
import {setupCsrfRequests} from "./util";


$(() => {
    let gameUuid = $("#game-data").data("uuid");
    let currentUsername = $("#current-user").data("name");
    let currentUserUuid = $("#current-user").data("uuid");
    let error = $("#error-data").data("error");
    setupCsrfRequests();

    ReactDOM.render(
        <div id="react-root">
            <SideDrawer pageName={APP_NAME} menuCategories={MENU_CATEGORIES}/>
            <ScAppBar appName={APP_NAME} httpService={$} currentUsername={currentUsername}/>
            <div id="content-wrapper">
                <div className="mui--appbar-height"></div>
                <Game
                    httpService={$}
                    userUuid={currentUserUuid}
                    gameUuid={gameUuid}
                    error={error}
                />
                <div className="footer-height"></div>
            </div>
            <Footer/>
        </div>,
        document.getElementById("content-root")
    );

    setupSideDrawerTransition();
});
