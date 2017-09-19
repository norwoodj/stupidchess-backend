import React from "react";
import {toTitleCase, toEnum} from "../util";


class UpdatingSelect extends React.Component {
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
        let value = toEnum(e.nativeEvent.srcElement.value);

        if (value == "ALL") {
            this.props.optionChangeHandler(null);
        } else {
            this.props.optionChangeHandler(value);
        }
    }

    render() {
        return this.state.options != null ? (
            <div className="mui-select">
                <label>{this.getSelectLabel()}</label>
                <select onChange={this.handleChangeEvent.bind(this)}>
                    {this.state.options.map(option => <option key={option}>{toTitleCase(option)}</option>)}
                </select>
            </div>
        ) : null;
    }
}

UpdatingSelect.propTypes = {
    optionChangeHandler: React.PropTypes.func.isRequired,
    options: React.PropTypes.array.isRequired,
    allOption: React.PropTypes.bool.isRequired
};

export {UpdatingSelect};
