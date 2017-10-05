import $ from "jquery";
import {GameType} from "./constants";


function toTitleCase(input) {
    return input.split("_")
        .map(str => str.charAt(0).toUpperCase() + str.substring(1).toLowerCase())
        .join(" ");
}

function range(size) {
    let range = [];
    for (let i = 0; i < size; ++i) {
        range[i] = i;
    }

    return range;
}

function setupCsrfRequests() {
    let csrfToken = $("#csrf-token").data("token");

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        }
    });
}

function isGameInBoardSetupMode(game) {
    return game.type == GameType.STUPID_CHESS && game.lastMove < 23;
}


export {toTitleCase, range, setupCsrfRequests, isGameInBoardSetupMode};