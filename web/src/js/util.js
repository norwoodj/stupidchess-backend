function toTitleCase(str) {
    return str.charAt(0).toUpperCase() + str.substring(1).toLowerCase();
}

function range(size) {
    let range = [];
    for (let i = 0; i < size; ++i) {
        range[i] = i;
    }

    return range;
}

function getQueryParam(parameter) {
    var match = new RegExp('[?&]' + parameter + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

export {toTitleCase, range, getQueryParam};