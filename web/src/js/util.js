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

export {toTitleCase, range};