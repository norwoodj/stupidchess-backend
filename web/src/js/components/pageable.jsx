import React from "react";
import Button from "muicss/lib/react/button";
import Form from "muicss/lib/react/form";
import Panel from "muicss/lib/react/panel";
import Container from "muicss/lib/react/container";

import {redirectToNextQueryParam, handleUnauthorized} from "../util";
import {FormErrors} from "./form-errors";


class Pageable extends React.Component {
    constructor() {
        super();

        this.state = {
            results
        };
    }

    render() {
        return (
            <div>
                <Button className="submit-button" onClick={this.handlePageBack.bind(this)} variant="raised">{"<"}</Button>
                <Button className="submit-button" onClick={this.handlePageForward.bind(this)} variant="raised">{">"}</Button>
                <Input
                    label="Other Player's name"
                    hint="Other Player's name"
                    required={true}
                    onChange={this.updateOtherPlayer.bind(this)}
                />
            </div>
        );
    }
}

export {AbstractForm};
