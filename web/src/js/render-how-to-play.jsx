import $ from "jquery";
import React from "react";
import ReactDOM from "react-dom";

import Container from "muicss/lib/react/container";
import Panel from "muicss/lib/react/panel";
import ScAppBar from "./components/app-bar";
import SideDrawer from "./components/side-drawer";
import Footer from "./components/footer";

import {setupSideDrawerTransition} from "./side-drawer-transition";
import {MENU_CATEGORIES, APP_NAME} from "./constants";
import {setupCsrfRequests} from "./util";


$(() => {
    let currentUsername = $("#current-user").data("name");
    setupCsrfRequests();

    ReactDOM.render(
        <div id="react-root">
            <SideDrawer pageName={APP_NAME} menuCategories={MENU_CATEGORIES}/>
            <ScAppBar appName={APP_NAME} httpService={$} currentUsername={currentUsername}/>
            <div id="content-wrapper">
                <div className="mui--appbar-height"></div>
                <Container className="main-container">
                    <Panel>
                        <h2>How To Play Stupid Chess</h2>
                        <div className="mui-divider"></div>
                        <br/>
                        <p>
                            Stupid Chess is a variant on the traditional checkers and chess board games. It is played on a chess
                            board that has been ripped in half, and realigned with half of each board half overlapping.
                        </p>
                        <p>
                            In addition to this change, Stupid Chess is played with a different set of pieces than traditional
                            chess. The complete set of pieces that each side starts with is as follows:
                        </p>
                        <ul>
                            <li>1 King</li>
                            <li>1 Queen</li>
                            <li>2 Castles</li>
                            <li>2 Bishops</li>
                            <li>1 Pony (called a Knight in traditional chess)</li>
                            <li>4 Pawns</li>
                            <li>1 Checker</li>
                        </ul>
                        <p>
                            When the Stupid Chess board has been set up to start the game, it might look like this:
                        </p>
                        <img src="/img/screenshots/after-board-setup.jpg"/>
                        <p>
                            Notice that the two sides are not set up exactly the same. That is because each player sets
                            up their board in secret however they want from the starting pieces before the game starts.
                            The next section will explain more.
                        </p>
                        <h3>Board Setup Mode</h3>
                        <p>
                            Before the game begins, each player takes their half of the board and sets up their starting
                            pieces in secret. If you're playing a 2 player game, you won't be able to see where the other
                            player has placed their pieces until both of you are done setting up.
                        </p>
                        <p>
                            The highlighted squares are the places where you need to place pieces. Click on one of them
                            and then select which piece to place there.
                        </p>
                        <img src="/img/screenshots/board-setup-mode.jpg"/>
                        <h3>Movement</h3>
                        <p>
                            Once both players have set up their side of the board, the game begins. Gameplay and movement in
                            Stupid Chess is generally the same as in regular chess except for a couple of quirks in the middle
                            board and the effect it has on pawns and checkers. It matters for these two pieces and only these
                            two pieces because they're the only pieces with a notion of "forward". This matters in the middle
                            board because once one of these pieces moves into the 8x4 middle board section it can move forward
                            in two senses.
                        </p>
                        <img src="/img/screenshots/pawn-move-middle-board.jpg"/>
                        <p>
                            As you can see, the black pawn has to get to the white side down and to the right and would have no
                            way to get there unless it could move in both of these "forward" directions. This principle works just
                            the same with checkers, though it is maybe a bit more counterintuitive in this example. Even the move
                            down and to the left is a legal forward move because it is forward in the left sense, even though
                            it's backward in the up sense. The only place a white checker can't move in this example is down
                            and to the right, because it does not make any progress towards the black pieces.
                        </p>
                        <img src="/img/screenshots/checker-move-middle-board.jpg"/>
                        <h3>Scoring</h3>
                        <p>
                            One strange thing you might notice in the examples above is that there is not only a score, but
                            veintitres has more points than echo. A major difference of Stupid Chess over chess is that it
                            dispenses with the system of check and checkmate. Instead, each player has a score assigned that
                            is calculated as the number of kings that that player has in play. In practice, this is no different
                            from chess rules with one major exception. By getting a checker to the end of the board, you get
                            your checker "kinged". A checker king counts the same as a chess king in your score, so if a player
                            like the one in the above examples gets a checker kinged, their score will increase by a point, and
                            the other player will have to capture both of their kings to win.
                        </p>
                        <p>
                            The most a player can win a game of Stupid Chess by is actually 6-0. This is because there is also
                            the pawn promotion rules of Chess, but you have the additional option of replacing a pawn with a
                            checker king, increasing your score again by one.
                        </p>
                        <img src="/img/screenshots/pawn-promotion.jpg"/>
                        <img src="/img/screenshots/pawn-promoted-checker-king.jpg"/>
                        <h3>Miscellaneous</h3>
                        <p>
                            That's pretty much it for the rules. There's still a few odd things here and there, like that you
                            are allowed to capture your own pieces:
                        </p>
                            <img src="/img/screenshots/self-capture.jpg"/>
                        <p>
                            Also, checkers can move twice on their first move because... they're like pawns I guess?
                        </p>
                        <img src="/img/screenshots/checker-move-twice.jpg"/>
                        <p>
                            Checker kings can move twice on their first move too. Don't worry too much about the rules.
                        </p>
                    </Panel>
                </Container>
            </div>
            <div className="footer-height"></div>
            <Footer/>
        </div>,
        document.getElementById("content-root")
    );

    setupSideDrawerTransition();
});
