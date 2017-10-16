
function getPieceImage(piece) {
    return `/img/pieces/${piece.color.toLowerCase()}/${piece.type.toLowerCase()}.svg`;
}

export {getPieceImage};
