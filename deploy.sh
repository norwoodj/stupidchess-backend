#!/bin/bash -e

source common.sh


function usage {
    echo "${0} <commands>"
    echo
    echo "Commands:"
    echo "  deploy_image <image>: Pushes built image to the configured docker registry"
    echo
    echo "Images:"
    echo "  all"
    echo "  frontend_code"
    echo "  nginx"
    echo "  server_code"
    echo "  uwsgi"
    echo
    echo "Options:"
    echo "  --help, -h, --?, -? Print this usage and exit"
}

function get_docker_registry_name {
    if [[ ! -z ${DOCKER_REGISTRY_URL} ]]; then
        printf ${DOCKER_REGISTRY_URL}
    else
        printf "Docker Hub"
    fi
}

function do_deploy_image {
    local image=${1}
    local version=`get_version ${image}`
    local image_tag=`get_image_tag ${image} ${version}`

    log_block "Deploying ${image_tag} image to $(get_docker_registry_name)"
    check_image_exists ${image} ${version}
    docker push ${image_tag}
}

function deploy_image {
    local image_name=${1}

    if [[ -z ${image_name} ]]; then
        usage
        exit 1
    fi

    if [[ ${image_name} = 'all' ]]; then
        images=`get_images_for_deploy`

        log_block 'Deploying all images:'
        for i in ${images}; do
            log_line "${i}"
        done

        for i in ${images}; do
            do_deploy_image ${i}
        done
    else
        do_deploy_image ${image_name}
    fi
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

    command=${1}
    arg=${2}
    ${command} ${arg}
}

main ${@}
