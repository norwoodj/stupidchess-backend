import React from "react";
import Button from "muicss/lib/react/button";
import Form from "muicss/lib/react/form";
import Panel from "muicss/lib/react/panel";
import Container from "muicss/lib/react/container";

import {redirectToNextQueryParam, handleUnauthorized} from "../util";
import {FormErrors} from "./form-errors";


class AbstractForm extends React.Component {
    constructor() {
        super();

        this.state = {
            errors: null
        };
    }

    errorCheck() {
        return true;
    }

    getLegend() {
        return "";
    }

    renderFormFields() {
        return "";
    }

    getFormRedirectDefault() {
        return "/";
    }

    handleSubmitFailure(error) {
        if (error.hasOwnProperty("responseJSON") && error.responseJSON.hasOwnProperty("message")) {
            this.setState({errors: error.responseJSON.message + "!"});
            return;
        }

        if (handleUnauthorized(error)) {
            return;
        }

        this.setState({errors: "Error submitting form, see console"});
        console.log(error);

    }

    handleSubmit(event) {
        event.preventDefault();

        if (!this.errorCheck()) {
            return;
        }

        this.submitForm().then(
            response => redirectToNextQueryParam(this.getFormRedirectDefault(response)),
            this.handleSubmitFailure.bind(this)
        );
    }

    render() {
        return (
            <Container className="form-container">
                <Panel>
                    <Form id="input-form">
                        <legend>{this.getLegend()}</legend>
                        {this.renderFormFields()}
                        <Button className="submit-button" onClick={this.handleSubmit.bind(this)} variant="raised">Submit</Button>
                    </Form>
                    {this.state.errors != null ? <FormErrors errors={this.state.errors}/> : ""}
                </Panel>
            </Container>
        );
    }
}

export {AbstractForm};
