import $ from "jquery";
import React from "react";
import ReactDOM from "react-dom";

import Container from "muicss/lib/react/container";
import ScAppBar from "./components/app-bar";
import SideDrawer from "./components/side-drawer";
import Footer from "./components/footer";
import Profile from "./components/profile";

import {setupSideDrawerTransition} from "./side-drawer-transition";
import {MENU_CATEGORIES, APP_NAME} from "./constants";
import {setupCsrfRequests} from "./util";


$(() => {
    let currentUsername = $("#current-user").data("name");
    let profileUserUuid = $("#profile-user").data("uuid");
    let profileUsername = $("#profile-user").data("name");
    let error = $("#error-data").data("error");

    setupCsrfRequests();

    ReactDOM.render(
        <div id="react-root">
            <SideDrawer pageName={APP_NAME} menuCategories={MENU_CATEGORIES}/>
            <ScAppBar
                appName={APP_NAME}
                httpService={$}
                currentUsername={currentUsername}
            />
            <div id="content-wrapper">
                <div className="mui--appbar-height"></div>
                <Container className="main-container">
                    <Profile
                        httpService={$}
                        profileUserUuid={profileUserUuid}
                        profileUsername={profileUsername}
                        error={error}
                    />
                </Container>
            </div>
            <div className="footer-height"></div>
            <Footer/>
        </div>,
        document.getElementById("content-root")
    );

    setupSideDrawerTransition();
});
