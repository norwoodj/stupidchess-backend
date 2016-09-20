#!/bin/bash -e

source common.sh


function usage {
    echo "${0} <command>"
    echo
    echo "Commands:"
    echo "  start: Run the local server for development"
    echo "  stop:  Kill the local development server, stops and removes the containers if they're running in "
    echo "         daemon mode, otherwise, will just remove the stopped containers"
    echo
    echo "Options:"
    echo "  --daemon, -d        Starts the local server in development mode, has no effect when stopping"
    echo "  --help, -h, --?, -? Print this usage and exit"
}

function build_docker_compose_template_data {
    local images=`get_images_for_local_run`

    echo '---'
    for i in ${images}; do
        local image_version=`get_version ${i}`
        echo "${i}${HANDLEBARS_VERSION_SUFFIX}: '${image_version}'"
    done
    echo "project_path: '`pwd`'"
    echo '---'
}

function render_mustache_template {
    local render_mustache_image_tag=`get_current_image_tag ${MUSTACHE_RENDER_IMAGE_NAME}`

    build_docker_compose_template_data | docker run \
        --rm \
        -v `pwd`:/opt/mustache \
        -w /opt/mustache \
        -i ${render_mustache_image_tag} \
        mustache - ${LOCAL_DOCKER_COMPOSE_MUSTACHE_FILE}
}

function run_docker_compose_for_images {
    command=${1}
    log_block 'Rendering docker-compose template with current image versions'
    build_image_if_not_exists ${MUSTACHE_RENDER_IMAGE_NAME}

    log_line 'Using docker-compose config:'

    log_border
    render_mustache_template
    log_border

    docker-compose \
      -f <(render_mustache_template) \
      ${command} \
      `[[ ${command} == 'up' && ${DAEMON} == 'true' ]] && echo '-d'`
}

function ensure_all_images_exist {
    log_block 'Ensuring all images for run exist'
    local images=`get_images_for_local_run`

    for i in ${images}; do
        check_image_exists ${i}
    done
}

function start {
    log_block 'Starting Server...'
    ensure_all_images_exist
    run_docker_compose_for_images 'up'
}

function stop {
    log_block 'Stopping Server...'
    run_docker_compose_for_images 'down'
}

function main {
    while [[ ${1} == -* ]]; do
        case ${1} in
            --daemon | -d )
                DAEMON="true"
            ;;
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
    ${command}
}


main ${@}
