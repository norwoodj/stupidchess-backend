import React from "react";
import PropTypes from "prop-types";
import UpdatingSelect from "../components/updating-select";
import {Color} from "../constants";


export default class ColorSetupSelect extends React.Component {
    render() {
        if (!this.props.gameState.inBoardSetupMode()) {
            return null;
        }

        return (
            <div id="color-setup-select" className="content-block game-page-select">
                <UpdatingSelect
                    label="Select Color to set up"
                    optionChangeHandler={this.props.colorChangeHandler}
                    options={Color.all()}
                />
            </div>
        );
    }
}

ColorSetupSelect.propTypes = {
    gameState: PropTypes.object.isRequired,
    boardSetupState: PropTypes.object.isRequired,
    colorChangeHandler: PropTypes.func.isRequired
};
