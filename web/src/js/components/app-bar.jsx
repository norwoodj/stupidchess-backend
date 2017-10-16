import React from "react";
import PropTypes from "prop-types";
import Appbar from "muicss/lib/react/appbar";
import Container from "muicss/lib/react/container";


export default class ScAppBar extends React.Component {
    constructor() {
        super();
        this.state = {
            user: null
        };
    }

    render() {
        return (
            <header id="header">
                <Appbar className="mui--appbar-line-height skin-element">
                    <Container fluid={true}>
                        <table width="100%"><tbody><tr>
                            <td>
                                <a className="sidedrawer-toggle mui--visible-xs-inline-block js-show-sidedrawer">☰</a>
                                <a className="sidedrawer-toggle mui--hidden-xs js-hide-sidedrawer">☰</a>
                                <a className="link mui--text-title mui--invisible-xs" href="/">{this.props.appName}</a>
                            </td>
                            <td className="mui--text-right mui--invisible-xs">{
                                this.props.currentUsername == null
                                    ? <div><a className="link" href="/login">Login</a> | <a className="link" href="/create-account">Create Account</a></div>
                                    : <div>Hello, <a className="link" href="/profile">{this.props.currentUsername}</a> | <a className="link" href="/logout">Logout</a></div>
                            }</td>
                        </tr></tbody></table>
                    </Container>
                </Appbar>
            </header>
        );
    }
}

ScAppBar.propTypes = {
    appName: PropTypes.string.isRequired,
    httpService: PropTypes.func.isRequired,
    currentUsername: PropTypes.string
};
