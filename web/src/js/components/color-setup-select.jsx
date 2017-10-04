import React from "react";
import PropTypes from "prop-types";
import {Color} from "../constants"
import {UpdatingSelect} from "../components/updating-select";


class ColorSetupSelect extends React.Component {
    render() {
        if (!this.props.gameState.inBoardSetupMode()) {
            return null;
        }

        return (
            <div id="color-setup-select" className="content-block mui-col-lg-12 mui-col-md-12 mui-col-sm-6 mui-col-xs-6">
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

export {ColorSetupSelect};
