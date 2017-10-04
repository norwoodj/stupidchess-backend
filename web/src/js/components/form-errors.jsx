import React from "react";
import PropTypes from "prop-types";

class FormErrors extends React.Component {

    constructor() {
        super();
    }

    render() {
        return this.props.errors !== ""
            ? <div className="error-text">{this.props.errors}</div>
            : "";
    }
}

FormErrors.propTypes = {
    errors: PropTypes.string.isRequired
};

export {FormErrors};
