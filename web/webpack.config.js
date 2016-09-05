const path = require('path');
const webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    entry: './src/js/game.jsx',
    resolve: {
        extensions: ['', '.js', '.jsx']
    },
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'js/bundle.js'
    },
    plugins: [
        new CopyWebpackPlugin([
            { from: 'src/html' },
            { from: 'src/css', to: 'css/' },
            { from: 'src/img', to: 'img/' }
        ])
    ],
    module: {
        preLoaders: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loaders: ['eslint']
            }
        ],
        loaders: [
            {
                test: /\.jsx?$/,
                loader: 'babel',
                exclude: /node_modules/
            }
        ]
    }
};
