
let MENU_CATEGORIES = [
    {
        category: "Pages",
        options: [
            {text: "Home", link: "/"},
            {text: "Create Game", link: "/create-game.html"}
        ]
    }
];

let APP_NAME = "Stupid Chess";

let GameType = {
    STUPID_CHESS: "STUPID_CHESS",
    CHESS: "CHESS",
    CHECKERS: "CHECKERS"
};

let GAME_TYPES = [
    GameType.STUPID_CHESS,
    GameType.CHESS,
    GameType.CHECKERS
];

let GameAuthType = {
    ANONYMOUS: "ANONYMOUS",
    SINGLE_PLAYER: "SINGLE_PLAYER",
    TWO_PLAYER: "TWO_PLAYER"
};

let GAME_AUTHORIZATION_TYPES = [
    GameAuthType.ANONYMOUS,
    GameAuthType.SINGLE_PLAYER,
    GameAuthType.TWO_PLAYER
];

export {
    GameType,
    GAME_TYPES,
    GameAuthType,
    GAME_AUTHORIZATION_TYPES,
    MENU_CATEGORIES,
    APP_NAME
};
