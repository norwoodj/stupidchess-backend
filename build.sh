#!/bin/bash -e

source common.sh


function usage {
    echo "${0} <images>"
    echo
    echo "Images:"
    echo "  all:             Build all assets and docker images needed to run the application"
    echo "  frontend_code:   Build the frontend code data image"
    echo "  nginx:           Build the nginx image"
    echo "  server_code:     Build the server code data image"
    echo "  uwsgi:           Build the uwsgi server image"
    echo "  webpack_builder: Build the webpack_builder image, which will be used to build frontend assets when building the frontend_code image"
}


function main {
    if [[ ${#} < 1 ]]; then
        usage
        exit 1
    fi

    if [[ ${1} = 'all' ]]; then
        local images=`get_images`
        log_block 'Building all images:'
        for i in ${images}; do
            log_line "${i}"
        done

        for i in ${images}; do
            build_image ${i}
            echo
        done
    else
        for i in ${@}; do
            build_image ${i}
            echo
        done
    fi
}


main ${@}
