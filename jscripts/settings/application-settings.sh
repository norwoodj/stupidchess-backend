#!/usr/bin/env bash

[[ -n "${_APPLICATION_SETTINGS_SH:+_}" ]] && return || readonly _APPLICATION_SETTINGS_SH=1

source ${SCRIPT_DIR}/settings/docker-settings.sh
source ${SCRIPT_DIR}/utilities/rpi-utilities.sh

##
# This is where you should define the names of every application that is built by this project, an application being some
# collection of docker containers that should run as an atomic unit. These names will be used in scripts throughout this
# project, for instance in the 'run-locally.sh' script, where you will specify one of these applications to be run
##
readonly STUPIDCHESS_APP_NAME="${PROJECT_NAME}"

readonly _APPLICATION_CONFIG=$(cat <<EOF
{
    "applications": ["${STUPIDCHESS_APP_NAME}"],
    "imagesToRunApp": {
        "${STUPIDCHESS_APP_NAME}": [
            "${NGINX_IMAGE_NAME}",
            "${UWSGI_IMAGE_NAME}"
             $(is_running_on_raspberry_pi || echo ", \"${WEBPACK_BUILDER_IMAGE_NAME}\"")
        ]
    }
}
EOF
)


function get_app_list {
    jq -r ".applications[]" <<< "${_APPLICATION_CONFIG}"
}

function print_app_usage_list {
    echo "  ${STUPIDCHESS_APP_NAME}  Stupidchess application"
}

function get_images_necessary_to_run_app {
    local app=${1}
    jq -r ".imagesToRunApp.${app}[]" <<< "${_APPLICATION_CONFIG}"
}

function get_current_application_version {
    get_image_version "any"
}
