import React from 'react';
import Button from 'muicss/lib/react/button';
import Form from 'muicss/lib/react/form';
import Input from 'muicss/lib/react/input';
import Panel from 'muicss/lib/react/panel';
import Container from 'muicss/lib/react/container';

import UserService from '../services/user-service';
import {redirectToNextQueryParam} from '../util';


class LoginForm extends React.Component {

    constructor() {
        super();

        this.username = '';
        this.password = '';
    }

    componentDidMount() {
        this.userService = new UserService(this.props.httpService);
    }

    handleSubmit(event) {
        event.preventDefault();
        if (this.username == '' || this.password == '') {
            return;
        }

        this.userService.login(this.username, this.password).then(
            redirectToNextQueryParam,
            error => console.log(error)
        );
    }

    updateUsername(event) {
        this.username = event.target.value;
    }
    
    updatePassword(event) {
        this.password = event.target.value;
    }
    
    render() {
        return (
            <Container className="form-container">
                <Panel>
                    <Form id="input-form">
                        <legend>Login</legend>
                        <Input
                            label="Username"
                            hint="username"
                            required={true}
                            onChange={this.updateUsername.bind(this)}
                        />
                        <Input
                            label="Password"
                            hint="password"
                            required={true}
                            onChange={this.updatePassword.bind(this)}
                        />
                        <Button className="submit-button" onClick={this.handleSubmit.bind(this)} variant="raised">Submit</Button>
                    </Form>
                </Panel>
            </Container>
        );
    }
}

LoginForm.propTypes = {
    httpService: React.PropTypes.func.isRequired
};

export {LoginForm};
