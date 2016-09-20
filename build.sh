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
    echo
    echo "Options:"
    echo "  --help, -h, --?, -? Print this usage and exit"
}


function main {
    while [[ ${1} == -* ]]; do
        case ${1} in
            -h | --h | --help | -? | --? )
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

    if [[ ${#} < 1 ]]; then
        usage
        exit 1
    fi

    if [[ ${1} = 'all' ]]; then
        local images=`get_images_for_build`
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
