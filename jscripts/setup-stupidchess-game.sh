#!/usr/bin/env bash

SCRIPT_DIR="$(cd `dirname ${BASH_SOURCE[0]}` && pwd -P)"
source ${SCRIPT_DIR}/settings/setup-stupidchess-game-settings.sh


function usage {
    echo "Usage:"
    echo "  ${BASH_SOURCE[0]} [options] <game-uuid>"
    echo
    echo "This script is used to set up a stupidchess game, skipping the board setup mode by placing the pieces"
    echo "for each the black and white sides"
    echo
    echo "Options:"
    print_options_usage_list
}

function setup_stupidchess_game {
    local game_uuid=${1}
    check_current_image_exists "${UWSGI_IMAGE_NAME}"

    docker run --rm -it \
        --entrypoint setup_stupidchess_game \
        "$(get_current_image_tag "${UWSGI_IMAGE_NAME}")" \
        ${SC_SETUP_SCRIPT_ARGS} \
        "${game_uuid}"
}

function main {
    local game_uuid=${1:-""}
    check_named_argument "Game UUID" "${game_uuid}" /dev/null "false"

    setup_stupidchess_game "${game_uuid}"
}

handle_options_and_pass_arguments_to_main ${@}

