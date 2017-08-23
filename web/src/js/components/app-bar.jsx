import React from 'react';
import Appbar from 'muicss/lib/react/appbar';
import Container from 'muicss/lib/react/container';


class ScAppBar extends React.Component {
    render() {
        return (
            <header id="header">
                <Appbar className="mui--appbar-line-height skin-element">
                    <Container fluid={true}>
                        <a className="sidedrawer-toggle mui--visible-xs-inline-block js-show-sidedrawer">☰</a>
                        <a className="sidedrawer-toggle mui--hidden-xs js-hide-sidedrawer">☰</a>
                        <span className="mui--text-title mui--visible-xs-inline-block">{this.props.appName}</span>
                    </Container>
                </Appbar>
            </header>
        );
    }
}

ScAppBar.propTypes = {
    appName: React.PropTypes.string.isRequired
};

export {ScAppBar};
