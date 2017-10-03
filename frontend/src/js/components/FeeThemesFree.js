import React, { Component } from 'react'

export default class FeeThemesFree extends Component {
  render() {
    if (this.props.themesFree) {
      return (
        <div className="badge-wrapper">
          <span className="badge badge-pill badge-success">Bonus</span>
          <span className="pricing-num-inline">
            Stockspot Themes
          </span>
        </div>
      );
    }
    return <div />;
  }
}
