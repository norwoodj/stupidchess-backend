import React from "react";

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
    errors: React.PropTypes.string.isRequired
};

export {FormErrors};
