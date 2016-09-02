#!/bin/bash

source common.sh


function usage {
    echo "${0} <commands>"
    echo
    echo "Commands:"
    echo "  server: Run the server container"
}

function server {
    log_block "Running Server Container"
    version=`get_web_version`
    docker run -p"8000:8000" -d "${SERVER_IMAGE_NAME}:${version}"
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
