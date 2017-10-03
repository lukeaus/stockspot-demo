import React, { Component } from 'react'

export default class MonthsFree extends Component {
  render() {
    if (this.props.monthsFree) {
      const monthsDisplay =  this.props.monthsFree > 1 ? 'months' : 'month';
      return (
        <div className="badge-wrapper">
          <span className="badge badge-pill badge-success">Bonus</span>
          <span className="pricing-num-inline">
            First {this.props.monthsFree} {monthsDisplay} free
          </span>
        </div>
      );
    }
    return <div />;
  }
}
