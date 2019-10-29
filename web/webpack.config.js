const path = require("path");
const webpack = require("webpack");
const CopyWebpackPlugin = require("copy-webpack-plugin");


module.exports = {
    entry: {
        changePassword: "./src/js/render-change-password-form.jsx",
        createAccount: "./src/js/render-create-account-form.jsx",
        createGame: "./src/js/render-game-form.jsx",
        index: "./src/js/render-index-page.jsx",
        howToPlay: "./src/js/render-how-to-play.jsx",
        game: "./src/js/render-game-page.jsx",
        login: "./src/js/render-login-form.jsx",
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
        new webpack.optimize.ModuleConcatenationPlugin(),
        new webpack.optimize.UglifyJsPlugin({minimize: true}),
        new CopyWebpackPlugin([
            {from: "src/_version.json"},
            {from: "src/css", to: "css/"},
            {from: "src/img", to: "img/"},
            {from: "src/favicons", to: "favicons/"},
            {from: "node_modules/react-table/react-table.css", to: "css/"}
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
