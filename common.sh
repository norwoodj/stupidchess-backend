#!/usr/bin/env bash

PROJECT_NAME='stupidchess'

WEB_PACKAGE_JSON_FILE='web/package.json'
SERVER_SETUP_PY_FILE='server/setup.py'

FRONTEND_DIRECTORY='web'
FRONTEND_ASSETS_DIRECTORY='dist'

DOCKERFILE_DIRECTORY='docker'
DOCKERFILE_PREFIX='Dockerfile-'

VERSION_FILE_DIRECTORY='versions'

UWSGI_VERSION_FILE="${VERSION_FILE_DIRECTORY}/uwsgi-image-version.txt"
NGINX_VERSION_FILE="${VERSION_FILE_DIRECTORY}/nginx-image-version.txt"
WEBPACK_BUILDER_VERSION_FILE="${VERSION_FILE_DIRECTORY}/webpack_builder-image-version.txt"

FRONTEND_CODE_IMAGE_NAME='frontend_code'
NGINX_IMAGE_NAME='nginx'
SERVER_CODE_IMAGE_NAME='server_code'
SERVER_TESTS_IMAGE_NAME='server_tests'
UWSGI_IMAGE_NAME='uwsgi'
WEBPACK_BUILDER_IMAGE_NAME='webpack_builder'

CONTAINER_WEB_ROOT='/var/lib/johnmalcolmnorwood/stupidchess'

LOCAL_COMPOSE_HANDLEBARS_FILE="${DOCKERFILE_DIRECTORY}/docker-compose-LCL.yml.handlebars"
HANDLEBARS_VERSION_SUFFIX='_version'


function log_block {
    echo "==> ${@}"
}

function log_line {
    echo "  + ${@}"
}

function get_images {
    ls "${DOCKERFILE_DIRECTORY}/" | \
    grep ${DOCKERFILE_PREFIX} | \
    grep -v ${WEBPACK_BUILDER_IMAGE_NAME} | \
    grep -v ${SERVER_TESTS_IMAGE_NAME} | \
    sed "s|${DOCKERFILE_PREFIX}||g"
}

function get_server_code_version {
    # setup.py files requre versions of the form '0.0.0.dev0' for dev versions, but we want it to be '0.0.0-dev' like package.json
    local dotted_version=`grep 'version=' ${SERVER_SETUP_PY_FILE} | sed "s|version='\(.*\)',|\1|"`

    if [[ ${dotted_version} = *dev* ]]; then
        printf ${dotted_version} | sed 's|\([0-9.]*\)\.dev.*|\1|' | xargs printf '%s-dev'
    else
        printf ${dotted_version}
    fi
}

function image_of_version_exists {
    local image_name=${1}
    local version=${2}

    local docker_image_tag="${PROJECT_NAME}-${image_name}:${version}"
    docker history -q ${docker_image_tag} &> /dev/null
}

function get_version {
    local name=${1}

    case ${name} in
        ${FRONTEND_CODE_IMAGE_NAME})
            jq -r '.version' ${WEB_PACKAGE_JSON_FILE}
        ;;
        ${NGINX_IMAGE_NAME})
            cat ${NGINX_VERSION_FILE}
        ;;
        ${SERVER_CODE_IMAGE_NAME})
            get_server_code_version
        ;;
        ${UWSGI_IMAGE_NAME})
            cat ${UWSGI_VERSION_FILE}
        ;;
        ${WEBPACK_BUILDER_IMAGE_NAME})
            cat ${WEBPACK_BUILDER_VERSION_FILE}
        ;;
    esac
}

function build_image {
    local image_name=${1}
    log_block "Building ${image_name} image"

    local version=`get_version ${image_name}`
    log_line "Building '${image_name}' version '${version}'"

    log_line "Building '${image_name}' assets before packaging image"
    build_assets ${image_name}

    local image_tag="${PROJECT_NAME}-${image_name}:${version}"
    log_line "Building '${image_name}' docker image, using tag '${image_tag}'"
    docker build -t ${image_tag} -f "${DOCKERFILE_DIRECTORY}/${DOCKERFILE_PREFIX}${image_name}" .
}

function build_frontend_assets {
    local webpack_builder_image_version=`get_version ${WEBPACK_BUILDER_IMAGE_NAME}`

    set +e
    if ! image_of_version_exists ${WEBPACK_BUILDER_IMAGE_NAME} ${webpack_builder_image_version}; then
        set -e
        log_line "${PROJECT_NAME}-${WEBPACK_BUILDER_IMAGE_NAME}:${webpack_builder_image_version} image doesn't exist locally, building..."
        build_image ${WEBPACK_BUILDER_IMAGE_NAME}
    else
        set -e
    fi

    docker run --rm -it \
        -v "`pwd`/web/src:${CONTAINER_WEB_ROOT}/src" \
        -v "`pwd`/web/dist:${CONTAINER_WEB_ROOT}/dist" \
        "${PROJECT_NAME}-${WEBPACK_BUILDER_IMAGE_NAME}:${webpack_builder_image_version}"
}


function build_assets {
    local name=${1}
    case ${name} in
        ${FRONTEND_CODE_IMAGE_NAME})
            build_frontend_assets
            log_line "Build '${name}' assets"
        ;;
        *)
            log_line 'Nothing to build'
        ;;
    esac
}
