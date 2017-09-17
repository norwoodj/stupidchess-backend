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

function getQueryParam(parameter) {
    let match = new RegExp("[?&]" + parameter + "=([^&]*)").exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, " "));
}

function handleUnauthorized(error) {
    if (error.status == 401) {
        window.location.replace(`/login.html?next=${encodeURIComponent(window.location.pathname)}`);
        return true;
    }

    return false;
}

function redirectToNextQueryParam(defaultNextLocation) {
    let link = getQueryParam("next");

    if (link == null) {
        window.location.replace(defaultNextLocation);
        return;
    }

    window.location.replace(link);
}


export {toTitleCase, range, getQueryParam, handleUnauthorized, redirectToNextQueryParam};