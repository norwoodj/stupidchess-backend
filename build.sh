#!/bin/bash

source common.sh

DOCKER_DIR='docker'
SERVER_DOCKER_FILE="${DOCKER_DIR}/Dockerfile-server"


function usage {
    echo "${0} <commands>"
    echo
    echo "Commands:"
    echo "  build:              Build all assets and docker images"
    echo "  build_server_image: Build just the server image"
}

function build_server_image {
    log_block "Building Server Image"
    version=`get_web_version`
    docker build -t "${SERVER_IMAGE_NAME}:${version}" -f ${SERVER_DOCKER_FILE} .
}

function build {
    log_block "Building ${PROJECT_NAME}..."
    version=${1}
    build_server_image
}

function main {
    if [[ ${#} < 1 ]]; then
        usage
        exit 1
    fi

    for c in ${@}; do
        ${c}
    done
}


main ${@}
