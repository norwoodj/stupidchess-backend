import React from "react";
import PropTypes from "prop-types";
import {toTitleCase} from "../util";


export default class UpdatingSelect extends React.Component {
    handleChangeEvent(e) {
        let value = e.nativeEvent.srcElement.value;

        if (value == "ALL") {
            this.props.optionChangeHandler(null);
        } else {
            this.props.optionChangeHandler(value);
        }
    }

    render() {
        return (
            <div className="mui-select">
                <label>{this.props.label}</label>
                <select onChange={this.handleChangeEvent.bind(this)}>
                    {this.props.allOption ? <option value="ALL" key="ALL">All</option> : ""}
                    {this.props.options.map(option => <option value={option} key={option}>{toTitleCase(option)}</option>)}
                </select>
            </div>
        );
    }
}

UpdatingSelect.propTypes = {
    label: PropTypes.string.isRequired,
    optionChangeHandler: PropTypes.func.isRequired,
    options: PropTypes.array.isRequired,
    allOption: PropTypes.bool
};
