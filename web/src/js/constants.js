
let MENU_CATEGORIES = [
    {
        category: "Pages",
        options: [
            {text: "Home", link: "/"},
            {text: "Create Game", link: "/create-game"},
            {text: "Change Password", link: "/change-password"},
            {text: "How to play Stupid Chess", link: "/how-to-play"}
        ]
    }
];

let APP_NAME = "Stupid Chess";

let Color = {
    BLACK: "BLACK",
    WHITE: "WHITE",

    all: () => [
        Color.BLACK,
        Color.WHITE
    ]
};

let GameType = {
    STUPID_CHESS: "STUPID_CHESS",
    CHESS: "CHESS",
    CHECKERS: "CHECKERS",

    all: () => [
        GameType.STUPID_CHESS,
        GameType.CHESS,
        GameType.CHECKERS
    ]
};

let GameAuthType = {
    ONE_PLAYER: "ONE_PLAYER",
    TWO_PLAYER: "TWO_PLAYER",

    all: () => [
        GameAuthType.ONE_PLAYER,
        GameAuthType.TWO_PLAYER,
    ]
};

let GameResult = {
    WIN: "WIN",
    LOSS: "LOSS"
};

export {
    Color,
    GameType,
    GameAuthType,
    GameResult,
    MENU_CATEGORIES,
    APP_NAME
};
