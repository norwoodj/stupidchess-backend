#!/usr/bin/env bash

PROJECT_NAME='stupidchess'
SERVER_IMAGE_NAME="${PROJECT_NAME}-server"
WEB_PACKAGE_JSON_FILE='web/package.json'

function get_web_version {
    jq -r '.version' ${WEB_PACKAGE_JSON_FILE}
}

function log_block {
    echo "-> ${@}"
}

function log_line {
    echo "==> ${@}"
}
