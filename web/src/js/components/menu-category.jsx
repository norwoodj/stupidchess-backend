import React from 'react';


class MenuCategory extends React.Component {
    render() {
        return (
              <ul>
                <li>
                    <strong>{this.props.name}</strong>
                    <ul>{this.props.menuOptions.map((option) =>
                        <li><a href={option.link}>{option.text}</a></li>
                    )}</ul>
                </li>
            </ul>
        );
    }
}

MenuCategory.propTypes = {
    menuOptions: React.PropTypes.array.isRequired,
    name: React.PropTypes.string.isRequired
};

export {MenuCategory};
