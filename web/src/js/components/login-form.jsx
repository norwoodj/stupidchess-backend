import React from "react";
import Input from "muicss/lib/react/input";

import {AbstractForm} from "./abstract-form";
import UserService from "../services/user-service";


class LoginForm extends AbstractForm {
    constructor() {
        super();

        this.username = "";
        this.password = "";
    }

    componentDidMount() {
        this.userService = new UserService(this.props.httpService);
    }

    errorCheck() {
        if (this.username == "" || this.password == "") {
            this.setState({errors: "Username and password must be provided to login!"});
            return false;
        }

        return true;
    }

    submitForm() {
        return this.userService.login(this.username, this.password);
    }

    updateUsername(event) {
        this.username = event.target.value;
    }

    updatePassword(event) {
        this.password = event.target.value;
    }

    getLegend() {
        return "Login"
    }

    getFormRedirectDefault() {
        return "/profile.html";
    }

    renderFormFields() {
        return [
            <Input
                key="0"
                name="username"
                label="Username"
                hint="username"
                required={true}
                onChange={this.updateUsername.bind(this)}
            />,
            <Input
                key="1"
                name="password"
                type="password"
                label="Password"
                hint="password"
                required={true}
                onChange={this.updatePassword.bind(this)}
            />
        ];
    }
}

LoginForm.propTypes = {
    httpService: React.PropTypes.func.isRequired
};

export {LoginForm};
