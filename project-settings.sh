#!/usr/bin/env bash -e

#
## Configuration settings for the project, setting up the name of the project, the locations of various important files,
## and the process used to version and build the various docker images the project builds and uses
#

# The name of the project. This value will prefix all built docker image names generated so that an image named 'image'
# will end up having a tag of ${PROJECT_NAME}-image:version
PROJECT_NAME='stupidchess'

# The docker directory is where all Dockerfiles and docker-compose yaml files will be placed. The Dockerfile prefix is
# a prefix that should be used when naming all Dockerfiles. Such that an image named 'image' will be built by a
# Dockerfile called 'Dockerfile-image' which is stored in the Dockerfile directory configured here
DOCKERFILE_DIRECTORY='docker'
DOCKERFILE_PREFIX='Dockerfile-'

# The name of the docker compose file used to run locally
LOCAL_DOCKER_COMPOSE_MUSTACHE_FILE="${DOCKERFILE_DIRECTORY}/docker-compose-LCL.yml.mustache"

# List of Docker Images that this project builds
FRONTEND_CODE_IMAGE_NAME='frontend_code'
NGINX_IMAGE_NAME='nginx'
SERVER_CODE_IMAGE_NAME='server_code'
SERVER_TESTS_IMAGE_NAME='server_tests'
UWSGI_IMAGE_NAME='uwsgi'
WEBPACK_BUILDER_IMAGE_NAME='webpack_builder'
MUSTACHE_RENDER_IMAGE_NAME='mustache_render'

# Configuration for rendering the docker-compose.yml.mustache files. First, the version suffix that each image version key in
# file has. For instance for an image named 'image' with version suffix _version, in the docker-compose mustache file
# will be the image tag: image:{{image_version}}
MUSTACHE_RENDER_IMAGE_NAME='jnorwood/mustache_render'
HANDLEBARS_VERSION_SUFFIX='_version'

# Docker deploy configuration. If the DOCKER_REGISTRY_URL is empty, will be pushed to docker hub. The user is the
# organization that the image will be pushed to, so the full push url will be DOCKER_REGISTRY_URL/DOCKER_REGISTRY_ORG/image:tag
DOCKER_REGISTRY_URL=
DOCKER_REGISTRY_ORG='jnorwood'


function get_images_for_local_run {
    printf "${SERVER_CODE_IMAGE_NAME} ${UWSGI_IMAGE_NAME} ${WEBPACK_BUILDER_IMAGE_NAME} ${NGINX_IMAGE_NAME}"
}

function get_images_for_build {
    printf "${SERVER_CODE_IMAGE_NAME} ${UWSGI_IMAGE_NAME} ${FRONTEND_CODE_IMAGE_NAME} ${NGINX_IMAGE_NAME}"
}

function get_images_for_deploy {
    get_images_for_build
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
        *)
            printf 'latest'
        ;;
    esac
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


#
## Version files for those images that will be versioned in text files, and the package.json file used for versioning
## the frontend code and the setup.py file used to version the backend code
#
VERSION_FILE_DIRECTORY='versions'
UWSGI_VERSION_FILE="${VERSION_FILE_DIRECTORY}/uwsgi-image-version.txt"
NGINX_VERSION_FILE="${VERSION_FILE_DIRECTORY}/nginx-image-version.txt"
WEB_PACKAGE_JSON_FILE='web/package.json'
SERVER_SETUP_PY_FILE='server/setup.py'

#
## Build and version retrieval implementations
#
function get_server_code_version {
    # setup.py files require versions of the form '0.0.0.dev0' for dev versions, but we want it to be '0.0.0-dev' like package.json
    local dotted_version=`grep 'version=' ${SERVER_SETUP_PY_FILE} | sed "s|version='\(.*\)',|\1|"`

    if [[ ${dotted_version} = *dev* ]]; then
        printf ${dotted_version} | sed 's|\([0-9.]*\)\.dev.*|\1|' | xargs printf '%s-dev'
    else
        printf ${dotted_version}
    fi
}


CONTAINER_WEB_ROOT='/var/lib/johnmalcolmnorwood/stupidchess'

function build_frontend_assets {
    build_image_if_not_exists ${WEBPACK_BUILDER_IMAGE_NAME}
    local webpack_builder_image_tag=`get_current_image_tag ${WEBPACK_BUILDER_IMAGE_NAME}`

    docker run --rm -it \
        -v "`pwd`/web/src:${CONTAINER_WEB_ROOT}/src" \
        -v "`pwd`/web/dist:${CONTAINER_WEB_ROOT}/dist" \
        ${webpack_builder_image_tag}
}
