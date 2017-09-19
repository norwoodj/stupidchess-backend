import React from "react";
import {UpdatingSelect} from "./updating-select"


class GameTypeSelect extends UpdatingSelect {
    getSelectLabel() {
        return "Filter By Game Type";
    }
}

GameTypeSelect.propTypes = {
    optionChangeHandler: React.PropTypes.func.isRequired,
    options: React.PropTypes.array.isRequired,
    allOption: React.PropTypes.bool.isRequired
};

export {GameTypeSelect};
