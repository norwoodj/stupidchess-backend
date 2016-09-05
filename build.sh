#!/bin/bash -e

source common.sh


function usage {
    echo "${0} <images>"
    echo
    echo "Images:"
    echo "  all:           Build all assets and docker images"
    echo "  frontend_code: Build the frontend code data image"
    echo "  server_code:   Build the server code data image"
    echo "  uwsgi:         Build the uwsgi server image"
}

function build_image {
    image_name=${1}
    log_block "Building ${image_name} Image"

    version=`get_version ${image_name}`
    log_line "Building '${image_name}' version '${version}'"

    log_line "Building '${image_name}' assets before packaging image"
    build_assets ${image_name}

    image_tag="${PROJECT_NAME}-${image_name}:${version}"
    log_line "Building '${image_name}' docker image, using tag '${image_tag}'"
    docker build -t ${image_tag} -f "${DOCKERFILE_DIRECTORY}/${DOCKERFILE_PREFIX}${image_name}" .
}

function main {
    if [[ ${#} < 1 ]]; then
        usage
        exit 1
    fi

    if [[ ${1} = 'all' ]]; then
        images=`get_images`
        for i in ${images}; do
            build_image ${i}
        done
    else
        for i in ${@}; do
            if [[ ${i} != 'all' ]]; then
                build_image ${i}
            fi
        done
    fi
}


main ${@}
