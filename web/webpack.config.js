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
        extensions: [".js", ".jsx"]
    },
    output: {
        path: path.join(__dirname, "dist"),
        filename: "js/[name].bundle.js"
    },
    plugins: [
        new webpack.optimize.UglifyJsPlugin({minimize: true}),
        new CopyWebpackPlugin([
            { from: "src/_version.json" },
            { from: "src/css", to: "css/" },
            { from: "src/img", to: "img/" },
            { from: "node_modules/react-table/react-table.css", to: "css/" }
        ])
    ],
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                enforce: "pre",
                loader: "eslint-loader",
                exclude: /node_modules/
            }, {
                test: /\.jsx?$/,
                loader: "babel-loader",
                exclude: /node_modules/
            }, {
                test: /\.json$/,
                loader: "json-loader"
            }
        ]
    }
};
