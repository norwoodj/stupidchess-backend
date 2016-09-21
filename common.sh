#!/usr/bin/env bash

#
## Common utilities used by all the tooling scripts
#

source project-settings.sh

#
## Logging Utilities
#
function log_block {
    echo
    echo "==> ${@}"
}

function log_line {
    echo "  + ${@}"
}

function log_border {
    echo '======================================================================'
}


#
## Docker utilities
#
function image_of_version_exists {
    local image_name=${1}
    local version=${2}

    local docker_image_tag=`get_image_tag ${image_name} ${version}`
    docker history -q ${docker_image_tag} &> /dev/null
}

function check_image_exists {
    local image=${1}
    local current_version=`get_version ${image}`
    local image_tag=`get_image_tag ${image} ${current_version}`
    log_line "Ensuring '${image_tag}' exists locally"

    if ! image_of_version_exists ${image} ${current_version}; then
        log_line "Image ${image_tag} doesn't exist, build first: './build.sh ${image}'"
        exit 1
    fi
}

function build_image_if_not_exists {
    local image_name=${1}

    local image_version=`get_version ${image_name}`
    local image_tag=`get_image_tag ${image_name} ${image_version}`

    set +e
    log_line "Ensuring ${image_tag} image exists locally, building if not"
    if ! image_of_version_exists ${image_name} ${image_version}; then
        set -e
        build_image ${image_name}
    else
        set -e
    fi
}

function get_image_name {
    local image_name=${1}
    printf "${PROJECT_NAME}-${image_name}"
}

function get_image_tag {
    local image_name=${1}
    local version=${2}
    local full_image_name=`get_image_name ${image_name}`
    local image_tag_without_repository="${full_image_name}:${version}"

    if [ ! -z ${DOCKER_REGISTRY_URL} ]; then
        printf "${DOCKER_REGISTRY_URL}/"
    fi

    if [[ ! -z ${DOCKER_REGISTRY_ORG} ]]; then
        printf "${DOCKER_REGISTRY_ORG}/"
    fi

    printf ${image_tag_without_repository}
}

function get_current_image_tag {
    local image_name=${1}
    local version=`get_version ${image_name}`

    get_image_tag ${image_name} ${version}
}


function build_image {
    local image_name=${1}

    log_block "Building ${image_name} image"

    local version=`get_version ${image_name}`
    log_line "Building '${image_name}' version '${version}'"

    log_line "Building '${image_name}' assets before packaging image"
    build_assets ${image_name}

    local image_tag=`get_image_tag ${image_name} ${version}`
    log_line "Building '${image_name}' docker image, using tag '${image_tag}'"
    docker build -t ${image_tag} -f "${DOCKERFILE_DIRECTORY}/${DOCKERFILE_PREFIX}${image_name}" .
}
