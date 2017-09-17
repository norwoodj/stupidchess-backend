import React from "react";
import Appbar from "muicss/lib/react/appbar";
import Container from "muicss/lib/react/container";
import UserService from "../services/user-service";
import {redirectToNextQueryParam} from "../util";


class ScAppBar extends React.Component {
    constructor() {
        super();
        this.state = {
            user: null
        }
    }

    componentDidMount() {
        this.userService = new UserService(this.props.httpService);
        this.userService.getCurrentUser().then(
            user => this.setState({
                user: user
            }),
            () => null
        );
    }

    handleLogout() {
        this.userService.logout().then(
            () => redirectToNextQueryParam("/")
        )
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
                                this.state.user == null
                                    ? <div><a className="mui--hidden-xs link" href="/login.html">Login</a> | <a className="mui--hidden-xs link" href="/create-account.html">Create Account</a></div>
                                    : <div>Hello, <a className="mui--hidden-xs link" href="/profile.html">{this.state.user.username}</a> | <a className="mui--hidden-xs link" onClick={this.handleLogout.bind(this)}>Logout</a></div>
                            }</td>
                        </tr></tbody></table>
                    </Container>
                </Appbar>
            </header>
        );
    }
}

ScAppBar.propTypes = {
    appName: React.PropTypes.string.isRequired,
    httpService: React.PropTypes.func.isRequired,
};

export {ScAppBar};
