import React from "react";
import Input from "muicss/lib/react/input";

import UserService from "../services/user-service";
import {AbstractForm} from "./abstract-form";


class CreateAccountForm extends AbstractForm {
    constructor() {
        super();

        this.username = "";
        this.password = "";
        this.confirmPassword = "";
    }

    componentDidMount() {
        this.userService = new UserService(this.props.httpService);
    }

    errorCheck() {
        if (this.username == "" || this.password == "" || this.confirmPassword == "") {
            this.setState({errors: "Username and matching passwords must be provided in create account request!"});
            return false;
        }

        if (this.password != this.confirmPassword) {
            this.setState({errors: "Passwords provided don't match!"});
            return false;
        }

        if (this.password != this.confirmPassword) {
            this.setState({errors: "Passwords provided don't match!"});
            return false;
        }
        if (this.password.length < 8) {
            this.setState({errors: "Passwords must be >= 8 characters"});
            return false;
        }

        return true;
    }

    submitForm() {
        return this.userService.createAccount(this.username, this.password);
    }

    getLegend() {
        return "Create Account";
    }

    getFormRedirectDefault() {
        return "/profile.html";
    }

    updateUsername(event) {
        this.username = event.target.value;
    }

    updatePassword(event) {
        this.password = event.target.value;
    }

    updateConfirmPassword(event) {
        this.confirmPassword = event.target.value;
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
            />,
            <Input
                key="2"
                name="confirm-password"
                type="password"
                label="Confirm Password"
                hint="confirm password"
                required={true}
                onChange={this.updateConfirmPassword.bind(this)}
            />
        ];
    }
}

CreateAccountForm.propTypes = {
    httpService: React.PropTypes.func.isRequired
};

export {CreateAccountForm};
