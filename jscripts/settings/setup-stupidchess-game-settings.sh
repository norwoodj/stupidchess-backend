#!/usr/bin/env bash

[[ -n "${_SETUP_STUPIDCHESS_GAME_SETTINGS_SH:+_}" ]] && return || readonly _SETUP_STUPIDCHESS_GAME_SETTINGS_SH=1

source ${SCRIPT_DIR}/utilities/command-line-utilities.sh
source ${SCRIPT_DIR}/utilities/docker-utilities.sh

: ${SC_SETUP_SCRIPT_ARGS:=""}


function print_additional_options_usage_list {
    echo "  --stupidchess, -s            Specify the stupidchess server to connect to"
    echo "  --black_username, -b         Specify the username of the black player"
    echo "  --black_password, -c         Specify the password of the black player"
    echo "  --white_username, -w         Specify the username of the white player"
    echo "  --white_password, -v         Specify the password of the white player"
}

function handle_additional_options {
    local option=${1}

    case "${option}" in
        --stupidchess | -s | \
        --black_username | -b | \
        --black_password | -c | \
        --white_username | -w ) SC_SETUP_SCRIPT_ARGS="${SC_SETUP_SCRIPT_ARGS} ${option} ${2}"; return 2 ;;
        --white_password |  -v) SC_SETUP_SCRIPT_ARGS="${SC_SETUP_SCRIPT_ARGS} --white_password ${2}"; return 2 ;;
        *)                      return 1 ;;
    esac
}
