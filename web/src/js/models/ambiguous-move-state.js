
export default class AmbiguousMoveState {
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
        var disambiguatingCaptures = this.disambiguatingCapturesBySquare.get(this.selectedAmbiguousDestination);
        return disambiguatingCaptures.includes(square);
    }

    clear() {
        this.disambiguatingCapturesBySquare.clear();
        this.selectedAmbiguousDestination = null;
    }
}
