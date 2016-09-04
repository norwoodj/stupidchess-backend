#!/usr/bin/env bash

PROJECT_NAME='stupidchess'

WEB_PACKAGE_JSON_FILE='web/package.json'
SERVER_SETUP_PY_FILE='server/setup.py'
DOCKERFILE_DIRECTORY='docker'
DOCKERFILE_PREFIX='Dockerfile-'
UWSGI_VERSION_FILE='uwsgi-image-version.txt'


function get_images {
    ls "${DOCKERFILE_DIRECTORY}/" | grep ${DOCKERFILE_PREFIX} | sed "s|${DOCKERFILE_PREFIX}||g"
}

function get_server_code_version {
    # setup.py files requre versions of the form '0.0.0.dev0' for dev versions, but we want it to be '0.0.0-dev' like package.json
    dotted_version=`grep 'version=' ${SERVER_SETUP_PY_FILE} | sed "s|version='\(.*\)',|\1|"`

    if [[ ${dotted_version} = *dev* ]]; then
        printf ${dotted_version} | sed 's|\([0-9.]*\)\.dev.*|\1|' | xargs printf '%s-dev'
    else
        printf ${dotted_version}
    fi
}

function get_version {
    name=${1}
    if [[ ${name} = 'web' ]]; then
        jq -r '.version' ${WEB_PACKAGE_JSON_FILE}
    elif [[ ${name} = 'server_code' ]]; then
        get_server_code_version
    elif [[ ${name} = 'uwsgi' ]]; then
        cat ${UWSGI_VERSION_FILE}
    fi
}


function log_block {
    echo "==> ${@}"
}

function log_line {
    echo "+ ${@}"
}
