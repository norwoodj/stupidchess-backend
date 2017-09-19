import React from "react";
import {UpdatingSelect} from "./updating-select"


class GameAuthTypeSelect extends UpdatingSelect {
    getSelectLabel() {
        return "How Many Players?";
    }
}

GameAuthTypeSelect.propTypes = {
    optionChangeHandler: React.PropTypes.func.isRequired,
    options: React.PropTypes.array.isRequired,
    allOption: React.PropTypes.bool.isRequired
};

export {GameAuthTypeSelect};
