import $ from "jquery";
import {GameType, Color} from "./constants";


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

let SETUP_SQUARES_FOR_COLOR = new Map([
    [Color.BLACK, new Set([0, 1, 2, 3, 10, 11, 12, 13, 20, 21, 22, 23])],
    [Color.WHITE, new Set([94, 95, 96, 97, 104, 105, 106, 107, 114, 115, 116, 117])]
]);

function isSquareInSetupZoneForColor(color, square) {
    return SETUP_SQUARES_FOR_COLOR.get(color).has(square);
}

function isGameInBoardSetupMode(game) {
    return game.type == GameType.STUPID_CHESS && game.lastMove < 23;
}

function getErrorMessage(errorResponse) {
    if (errorResponse.status >= 500) {
        return "Unknown Server Error occurred. This means something's down, or John is a bad programmer, sorry";
    } else if (errorResponse.status == 404) {
        return "The resource that was requested does not exist!";
    } else if (errorResponse.status >= 400 && errorResponse.responseJSON && errorResponse.responseJSON.message) {
        return errorResponse.responseJSON.message;
    } else {
        console.log(errorResponse);
        return "Unknown error occurred, check the console for details";
    }
}

export {
    toTitleCase,
    range,
    setupCsrfRequests,
    isGameInBoardSetupMode,
    getErrorMessage,
    isSquareInSetupZoneForColor
};