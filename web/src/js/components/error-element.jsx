import React from "react";


class ErrorElement extends React.Component {
    render() {
        if (!this.props.error) {
            return null;
        }

        return <div className="mui--appbar-height error-bar"><div>{this.props.error}</div></div>;
    }
}

ErrorElement.propTypes = {
    error: React.PropTypes.string
};

export {ErrorElement};
