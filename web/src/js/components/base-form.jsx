import React from "react";
import ReactHtmlParser from "react-html-parser"
import Button from "muicss/lib/react/button";
import Form from "muicss/lib/react/form";
import Panel from "muicss/lib/react/panel";
import Container from "muicss/lib/react/container";


class BaseForm extends React.Component {
    render() {
        return (
            <Container className="form-container">
                <Panel>
                    <Form id="input-form" className="mui-form" method="POST">
                        <legend>{this.props.legend}</legend>
                        {ReactHtmlParser(this.props.formInnerHtml)}
                        <Button className="button" variant="raised">Submit</Button>
                    </Form>
                </Panel>
            </Container>
        );
    }
}


BaseForm.propTypes = {
    legend: React.PropTypes.string.isRequired,
    formInnerHtml: React.PropTypes.string.isRequired
};

export {BaseForm};
