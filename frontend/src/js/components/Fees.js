import React, { Component } from 'react';
import { connect } from 'react-redux';
import * as _debounce from 'lodash/debounce';
import Dots from 'react-activity/lib/Dots';

import { updateAmountInput, amountInputChanged } from '../actions';
import { MIN_INVEST_AMOUNT, FEES_ROUNDING_PLACES } from '../constants';
import { round, humanize } from '../utils/number';
import FeePlans from './FeePlans';
import FeeAverageSavingsFinePrint from './FeeAverageSavingsFinePrint';
import FeeMonthsFree from './FeeMonthsFree';
import FeeThemesFree from './FeeThemesFree';

const FEES_RESULT_DEBOUNCE_MS = 700;

class Fees extends Component {
  constructor(props) {
    super(props);
    this.state = {
      amountInput: '',
      feePeriodMonthly: true
    };
    this.updateAmountInput = _debounce.default(this.props.updateAmountInput,
      FEES_RESULT_DEBOUNCE_MS);
  }

  handleAmountInput(event) {
    event.persist();
    const amountInput = event.target.value.match(/\d+/g) || '';

    if (!amountInput && this.state.amountInput) {
      // cover case where user deletes the last remaining character in field
      this.setState({ amountInput });
    } else if (amountInput && amountInput[0] != this.state.amountInput[0]) {
      // don't trigger an amount changing if user didn't add a digit
      this.setState({ amountInput });
      this.props.amountInputChanged();
      this.updateAmountInput(amountInput);
    }
  }

  renderFeeAmount() {
    switch(this.props.feeCalcComplete) {
    case false:
      return <Dots size={20} />;
    case true:
      if (this.props.monthlyFee) {
        return (
          <div>
            <span className="pricing-label">Monthly Fee</span>
            <span className="pricing-num-inline">${humanize(this.props.monthlyFee)}</span>
            <span> per month</span>
          </div>
        );
      }
      if (this.state.amountInput && this.state.amountInput < MIN_INVEST_AMOUNT) {
        return <div>The minimum investment amount is ${MIN_INVEST_AMOUNT}</div>;
      }
    }
  }

  renderFeeMonthsFree() {
    if (this.props.feeCalcComplete && this.props.feePlan) {
      return <FeeMonthsFree monthsFree={this.props.feePlan.monthsFree} />;
    }
  }

  renderThemesFree() {
    if (this.props.feeCalcComplete && this.props.feePlan) {
      return <FeeThemesFree themesFree={this.props.feePlan.themesFree} />;
    }
  }

  shouldRenderAverageSavings() {
    return this.props.feeCalcComplete && this.props.feePlan && this.props.feePlan.avgSavingsRatio;
  }

  renderAverageSavingsFinePrint() {
    if (this.shouldRenderAverageSavings()) {
      return <FeeAverageSavingsFinePrint />;
    }
  }

  renderAverageSavings() {
    if (this.shouldRenderAverageSavings()) {
      // TODO: move this logic out of the component...
      let avgSavings = this.props.monthlyFee * this.props.feePlan.avgSavingsRatio;
      avgSavings = humanize(round(avgSavings, FEES_ROUNDING_PLACES));
      return (
        <div>
          <span className="pricing-label">Fees Saved</span>
          <span className="pricing-num-inline">${avgSavings} per month*</span>
        </div>
      );
    }
  }

  render() {
    return (
      <div id="fees">
        <h4 className="text-center">Fees</h4>
        <div className="row justify-content-center align-items-center">
          <div className="col input-group text-center" id="amount-input-group">
            <span className="input-group-addon">$</span>
            <input
              className="form-control"
              value={this.state.amountInput}
              onChange={this.handleAmountInput.bind(this)} />
          </div>
        </div>
        <div className="row justify-content-center align-items-center">
          <div className="col text-center" id="fees-calc">
            {this.renderFeeAmount()}
            {this.renderAverageSavings()}
            {this.renderFeeMonthsFree()}
            {this.renderThemesFree()}
            {this.renderAverageSavingsFinePrint()}
          </div>
        </div>
        <div className="row justify-content-center align-items-center">
          <div className="col">
            <FeePlans
              feePlan={this.props.feePlan}
              renderAverageSavingsFinePrint={this.renderAverageSavingsFinePrint.bind(this)}
            />
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = ({ monthlyFee, feePlan, feeCalcComplete }) => {
  return { monthlyFee, feePlan, feeCalcComplete };
};

export default connect(mapStateToProps, { updateAmountInput, amountInputChanged })(Fees);
