const path = require("path");
const webpack = require("webpack");
const CopyWebpackPlugin = require("copy-webpack-plugin");

module.exports = {
    entry: {
        game: "./src/js/render-game-page.jsx",
        createGame: "./src/js/render-game-form.jsx",
        login: "./src/js/render-login-form.jsx",
        createAccount: "./src/js/render-create-account-form.jsx",
        changePassword: "./src/js/render-change-password-form.jsx",
        profile: "./src/js/render-profile-page.jsx"
    },
    resolve: {
        extensions: ["", ".js", ".jsx"]
    },
    output: {
        path: path.join(__dirname, "dist"),
        filename: "js/[name].bundle.js"
    },
    plugins: [
        new CopyWebpackPlugin([
            { from: "src/_version.json" },
            { from: "src/css", to: "css/" },
            { from: "src/img", to: "img/" }
        ])
    ],
    module: {
        preLoaders: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loaders: ["eslint"]
            }
        ],
        loaders: [
            {
                test: /\.jsx?$/,
                loader: "babel",
                exclude: /node_modules/
            }, {
                test: /\.json$/,
                loader: 'json'
            }
        ]
    }
};
