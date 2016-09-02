import React from 'react';
import {toTitleCase} from '../util';


class ColorSetupSelect extends React.Component {
    render() {
        console.log('ColorSetupSelect');
        if (!this.props.gameState.inBoardSetupMode()) {
            return null;
        }

        return (
            <form>
                <div className="mui-select">
                    <label>Select Color to set up</label>
                    <select
                        onChange={e => this.props.colorChangeHandler(e.nativeEvent.srcElement.value.toUpperCase())}
                        value={toTitleCase(this.props.boardSetupState.getCurrentBoardBeingSetUp())}>
                        {this.props.gameState.getColorsSettingUp().map(color => <option key={color}>{toTitleCase(color)}</option>)}
                    </select>
                </div>
            </form>
        );
    }
}

ColorSetupSelect.propTypes = {
    gameState: React.PropTypes.object.isRequired,
    boardSetupState: React.PropTypes.object.isRequired,
    colorChangeHandler: React.PropTypes.func.isRequired
};

export {ColorSetupSelect};
