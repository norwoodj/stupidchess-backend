import React from "react";
import Input from "muicss/lib/react/input";

import UserService from "../services/user-service";
import {AbstractForm} from "./abstract-form";


class ChangePasswordForm extends AbstractForm {
    constructor() {
        super();

        this.username = "";
        this.password = "";
        this.newPassword = "";
        this.confirmNewPassword = "";
    }

    componentDidMount() {
        this.userService = new UserService(this.props.httpService);
    }

    errorCheck() {
        if (this.username == "" || this.password == "" || this.newPassword == "" || this.confirmNewPassword == "") {
            this.setState({errors: "Username, old password and matching new passwords must be provided in change password request!"});
            return false;
        }

        if (this.newPassword != this.confirmNewPassword) {
            this.setState({errors: "New Passwords provided don't match!"});
            return false;
        }

        if (this.newPassword.length < 8) {
            this.setState({errors: "Passwords must be >= 8 characters"});
            return false;
        }

        return true;
    }

    submitForm() {
        return this.userService.changePassword(this.username, this.password, this.newPassword);
    }

    getLegend() {
        return "Change Password";
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

    updateNewPassword(event) {
        this.newPassword = event.target.value;
    }

    updateConfirmNewPassword(event) {
        this.confirmNewPassword = event.target.value;
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
                name="new-password"
                type="password"
                label="New Password"
                hint="new password"
                required={true}
                onChange={this.updateNewPassword.bind(this)}
            />,
            <Input
                key="3"
                name="confirm-new-password"
                type="password"
                label="Confirm New Password"
                hint="confirm new password"
                required={true}
                onChange={this.updateConfirmNewPassword.bind(this)}
            />
        ];
    }
}

ChangePasswordForm.propTypes = {
    httpService: React.PropTypes.func.isRequired
};

export {ChangePasswordForm};
