import React from "react";
import PropTypes from "prop-types";
import {toTitleCase} from "../util";


export default class UpdatingSelect extends React.Component {
    constructor() {
        super();
        this.state = {
            options: null
        };
    }

    componentDidMount() {
        this.setState({options: this.props.allOption ? ["ALL", ...this.props.options] : this.props.options});
    }

    handleChangeEvent(e) {
        let value = e.nativeEvent.srcElement.value;

        if (value == "ALL") {
            this.props.optionChangeHandler(null);
        } else {
            this.props.optionChangeHandler(value);
        }
    }

    render() {
        return this.state.options != null ? (
            <div className="mui-select">
                <label>{this.props.label}</label>
                <select onChange={this.handleChangeEvent.bind(this)}>
                    {this.state.options.map(option => <option value={option} key={option}>{toTitleCase(option)}</option>)}
                </select>
            </div>
        ) : null;
    }
}

UpdatingSelect.propTypes = {
    label: PropTypes.string.isRequired,
    optionChangeHandler: PropTypes.func.isRequired,
    options: PropTypes.array.isRequired,
    allOption: PropTypes.bool
};
