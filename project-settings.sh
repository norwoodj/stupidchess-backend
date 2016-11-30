#!/bin/bash -e

#
## Configuration settings for the project, setting up the name of the project, the locations of various important files,
## and the process used to version and build the various docker images the project builds and uses
#

# The name of the project. This value will prefix all built docker image names generated so that an image named 'image'
# will end up having a tag of ${PROJECT_NAME}-image:version
PROJECT_NAME='stupidchess'
LOCAL_IMAGE_VERSION_TAG='current'

# Configuration for rendering the docker-compose.yml.mustache files. First, the version suffix that each image version key in
# file has. For instance for an image named 'image' with version suffix _version, in the docker-compose mustache file
# will be the image tag: image:{{image_version}}
MUSTACHE_RENDER_IMAGE_NAME='jnorwood/mustache_render'
HANDLEBARS_VERSION_SUFFIX='_version'
HANDLEBARS_ENV_SUFFIX='_environment'

# Docker deploy configuration. If the DOCKER_REGISTRY_URL is empty, will be pushed to docker hub. The user is the
# organization that the image will be pushed to, so the full push url will be DOCKER_REGISTRY_URL/DOCKER_REGISTRY_ORG/image:tag
DOCKER_REGISTRY_URL=
DOCKER_REGISTRY_ORG='jnorwood'

# Deployed App bundle name
DEPLOYED_APP_BUNDLE_NAME="${PROJECT_NAME}-current"
SERVER_BUNDLE_DEPLOY_DESTINATION="/var/lib/johnmalcolmnorwood/${PROJECT_NAME}"
# The name of the project. This value will prefix all built docker image names generated so that an image named 'image'
# will end up having a tag of ${PROJECT_NAME}-image:version


#
## Script Usage Configuration
#
function print_build_usage_images_list {
    echo "  all                Build all assets and docker images needed to run the application"

    if is_running_on_raspberry_pi; then
        echo "  rpi_frontend_code  Build the raspberry pi frontend code data image"
        echo "  rpi_nginx          Build the raspberry pi nginx image"
        echo "  rpi_server_code    Build the raspberry pi server code data image"
        echo "  rpi_uwsgi          Build the raspberry pi uwsgi server image"
    else
        echo "  frontend_code      Build the frontend code data image"
        echo "  nginx              Build the nginx image"
        echo "  server_code        Build the server code data image"
        echo "  uwsgi              Build the uwsgi server image"
    fi
}

function print_deploy_usage_images_list {
    echo "  all                Deploy all assets and docker images needed to run the application"
    echo "  rpi_frontend_code  Deploy the frontend code data image"
    echo "  rpi_nginx          Deploy the nginx image"
    echo "  rpi_server_code    Deploy the server code data image"
    echo "  rpi_uwsgi          Deploy the uwsgi server image"
}

function print_environment_list {
    :
}

function print_run_local_usage_services_list {
    echo "  stupidchess  Run the stupidchess web server"
}


#
## Build Configuration
#

# List of Docker Images that this project builds
FRONTEND_CODE_IMAGE_NAME='frontend_code'
NGINX_IMAGE_NAME='nginx'
SERVER_CODE_IMAGE_NAME='server_code'
SERVER_TESTS_IMAGE_NAME='server_tests'
UWSGI_IMAGE_NAME='uwsgi'
WEBPACK_BUILDER_IMAGE_NAME='webpack_builder'

RPI_FRONTEND_CODE_IMAGE_NAME='rpi_frontend_code'
RPI_NGINX_IMAGE_NAME='rpi_nginx'
RPI_SERVER_CODE_IMAGE_NAME='rpi_server_code'
RPI_UWSGI_IMAGE_NAME='rpi_uwsgi'
RPI_WEBPACK_BUILDER_IMAGE_NAME='rpi_webpack_builder'


function get_images_for_build {
    if is_running_on_raspberry_pi; then
        printf "${RPI_FRONTEND_CODE_IMAGE_NAME} ${RPI_NGINX_IMAGE_NAME} ${RPI_SERVER_CODE_IMAGE_NAME} ${RPI_UWSGI_IMAGE_NAME}"
    else
        printf "${FRONTEND_CODE_IMAGE_NAME} ${NGINX_IMAGE_NAME} ${SERVER_CODE_IMAGE_NAME} ${UWSGI_IMAGE_NAME}"
    fi
}

function get_images_for_deploy {
    printf "${RPI_FRONTEND_CODE_IMAGE_NAME} ${RPI_NGINX_IMAGE_NAME} ${RPI_SERVER_CODE_IMAGE_NAME} ${RPI_UWSGI_IMAGE_NAME}"
}

function get_services_for_deploy {
    printf ${PROJECT_NAME}
}

function get_images_for_service {
    local service=${1}
    if is_running_on_raspberry_pi; then
        printf "${RPI_WEBPACK_BUILDER_IMAGE_NAME} ${RPI_NGINX_IMAGE_NAME} ${RPI_SERVER_CODE_IMAGE_NAME} ${RPI_UWSGI_IMAGE_NAME}"
    else
        printf "${WEBPACK_BUILDER_IMAGE_NAME} ${NGINX_IMAGE_NAME} ${SERVER_CODE_IMAGE_NAME} ${UWSGI_IMAGE_NAME}"
    fi
}

function get_dockerfile_path_for_image {
    local image=${1}
    printf "docker/Dockerfile-${image}"
}

function get_docker_build_context_path_for_image {
    local image=${1}
    printf '.'
}

function get_docker_build_args_for_image {
    local image=${1}
}

function get_local_docker_compose_path_for_service {
    local service=${1}

    if is_running_on_raspberry_pi; then
        printf "docker/docker-compose-rpi.yml"
    else
        printf "docker/docker-compose.yml"
    fi
}

function get_image_version {
    local name=${1}

    case ${name} in
        ${RPI_FRONTEND_CODE_IMAGE_NAME})
            jq -r '.version' ${WEB_PACKAGE_JSON_FILE}
        ;;
        ${RPI_NGINX_IMAGE_NAME})
            cat ${NGINX_VERSION_FILE}
        ;;
        ${RPI_SERVER_CODE_IMAGE_NAME})
            get_setup_py_code_version 'server/setup.py'
        ;;
        ${RPI_UWSGI_IMAGE_NAME})
            cat ${UWSGI_VERSION_FILE}
        ;;
        *)
            printf 'latest'
        ;;
    esac
}


#
## Hooks
#

function pre_build_hook {
    local image_name=${1}
    log_block "Pre build hook for image ${image_name}"

    case ${image_name} in
        ${FRONTEND_CODE_IMAGE_NAME}|${RPI_FRONTEND_CODE_IMAGE_NAME})
            build_frontend_assets
            log_line "Built '${image_name}' assets"
        ;;
        *)
            log_line 'Nothing to build'
        ;;
    esac
}

function post_build_hook {
    local image_name=${1}
    log_block "Post build hook for image ${image_name}"
}

function pre_run_local_hook {
    local service=${1}
    log_block "Pre run local hook for service ${service}"
}

function post_run_local_hook {
    local service=${1}
    log_block "Post run local hook for service ${service}"
}


#
## Implementations
#

VERSION_FILE_DIRECTORY='versions'
UWSGI_VERSION_FILE="${VERSION_FILE_DIRECTORY}/uwsgi-image-version.txt"
NGINX_VERSION_FILE="${VERSION_FILE_DIRECTORY}/nginx-image-version.txt"
WEB_PACKAGE_JSON_FILE='web/package.json'
SERVER_SETUP_PY_FILE='server/setup.py'

function is_running_on_raspberry_pi {
    uname -a | grep 'arm' &> /dev/null
}

function get_setup_py_code_version {
    local setup_py_file_path=${1}
    printf `grep 'version=' ${setup_py_file_path} | sed "s|version='\(.*\)',|\1|"`
}

CONTAINER_WEB_ROOT='/var/lib/johnmalcolmnorwood/stupidchess'

function build_frontend_assets {
    local webpack_builder_image_name=''

    if is_running_on_raspberry_pi; then
        webpack_builder_image_name=${RPI_WEBPACK_BUILDER_IMAGE_NAME}
    else
        webpack_builder_image_name=${WEBPACK_BUILDER_IMAGE_NAME}
    fi

    build_image_if_not_exists ${webpack_builder_image_name}
    local webpack_builder_image_tag=`get_current_image_tag ${webpack_builder_image_name}`

    docker run --rm -it \
        -v "`pwd`/web/src:${CONTAINER_WEB_ROOT}/src" \
        -v "`pwd`/web/dist:${CONTAINER_WEB_ROOT}/dist" \
        ${webpack_builder_image_tag}
}
