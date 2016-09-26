class AmbiguousMoveState {
    constructor() {
        this.disambiguatingCapturesBySquare = new Map();
        this.selectedAmbiguousDestination = null;
    }

    isAmbiguousDestinationSelected() {
        return this.selectedAmbiguousDestination != null;
    }

    getSelectedAmbiguousDestination() {
        return this.selectedAmbiguousDestination;
    }

    selectAmbiguousDestination(square) {
        this.selectedAmbiguousDestination = square;
    }

    addAmbiguousMove(square, disambiguatingCaptures) {
        this.disambiguatingCapturesBySquare.set(square, disambiguatingCaptures);
    }

    isAmbiguousDestination(square) {
        return this.disambiguatingCapturesBySquare.has(square);
    }

    isDisambiguatingCaptureForSelectedSquare(square) {
        return this.disambiguatingCapturesBySquare.get(this.selectedAmbiguousDestination).includes(square);
    }

    clear() {
        this.disambiguatingCapturesBySquare.clear();
    }
}

export {AmbiguousMoveState};
