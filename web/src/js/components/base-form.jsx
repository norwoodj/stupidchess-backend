import React from "react";
import PropTypes from "prop-types";
import ReactHtmlParser from "react-html-parser";
import Button from "muicss/lib/react/button";
import Form from "muicss/lib/react/form";
import Panel from "muicss/lib/react/panel";


export default class BaseForm extends React.Component {
    render() {
        return (
            <Panel>
                <Form id="input-form" className="mui-form" method="POST">
                    <legend>{this.props.legend}</legend>
                    {ReactHtmlParser(this.props.formInnerHtml)}
                    <Button className="button" variant="raised">Submit</Button>
                </Form>
            </Panel>
        );
    }
}


BaseForm.propTypes = {
    legend: PropTypes.string.isRequired,
    formInnerHtml: PropTypes.string.isRequired
};
