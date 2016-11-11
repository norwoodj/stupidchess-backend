#!/usr/bin/env bash -e

source common.sh

function usage {
    echo "${0}"
    echo "  Runs the tests for the stupidchess server"
    echo
    echo "Options:"
    echo "  --help, -h  Print this usage and exit"
}

function main {
    while [[ ${1} == -* ]]; do
        case ${1} in
            -h | -h | --help )
                usage
                exit 0
            ;;
            -* )
                usage
                exit 1
            ;;
        esac
        shift
    done

    log_block "Running tests..."
    build_image_if_not_exists ${SERVER_CODE_IMAGE_NAME}
    local server_code_image_tag=`get_current_image_tag ${SERVER_CODE_IMAGE_NAME}`

    docker run --rm -i \
        -w /var/lib/johnmalcolmnorwood/stupidchess/server/src \
        -v `pwd`/server:/var/lib/johnmalcolmnorwood/stupidchess/server \
        --entrypoint nosetests \
        ${server_code_image_tag}
}

main ${@}
