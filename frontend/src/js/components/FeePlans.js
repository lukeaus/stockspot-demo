import React, { Component } from 'react';
import * as _map from 'lodash/map';
import { Card, CardHeader, CardText } from 'material-ui/Card';

import { FEES, MANAGEMENT_FEE_TYPE_PCT, MANAGEMENT_FEE_TYPE_FLAT } from '../constants';
import { round, humanize } from '../utils/number';
import FeeAverageSavingsFinePrint from './FeeAverageSavingsFinePrint';
import FeeMonthsFree from './FeeMonthsFree';
import FeeThemesFree from './FeeThemesFree';

export default class FeePlans extends Component {
  constructor(props) {
    super(props);
  }

  getManagementFeeDisplayTypePct(feePlan) {
    const decimalComp = feePlan.managementFeeMonthly.toString().split('.')[1];
    // rounding required due to JS float craziness
    // decimalComp.length - 2 because we are * 100 to get a percentage
    return round(feePlan.managementFeeMonthly * 100, decimalComp.length - 2) + '%';
  }

  getManagementFeeDisplay(feePlan) {
    switch(feePlan.managementFeeType) {
    case MANAGEMENT_FEE_TYPE_FLAT:
      return '$' + round(feePlan.managementFeeMonthly);
    case MANAGEMENT_FEE_TYPE_PCT:
      return this.getManagementFeeDisplayTypePct(feePlan);
    }
  }

  getAvgSavings(feePlan) {
    // TODO: Implement. Things to consider:
    //   - Do on average or on max in range
    //   - How do you want to display for max range
    return <span>$lorem.ipsum</span>;
  }

  renderPlan(feePlan, feePlanName) {
    const isApplicableFeePlan = (this.props.feePlan === feePlan);
    const minInvest = feePlan.minInvestAmount;
    const maxInvest = feePlan.maxInvestAmount;

    const cardStyle = {
      // transparent default border being used to stop bad transition to solid border
      // but doesn't look great
      border: isApplicableFeePlan ? '1px solid #BBBBBB' : '1px solid transparent',
      boxShadow: isApplicableFeePlan ? '0px 12px 24px -3px #999B9D' : ''
    };

    return (
      <div className="col" key={feePlanName}>
        <Card
          className="pricing-card"
          style={cardStyle}
        >
          <CardHeader
            className="pricing-card-header text-center"
            title={feePlanName}
            style={{ backgroundColor: feePlan.color, fontWeight: 'bold' }}
          />
          <div className="text-center">
            <CardText>
              <div className="pricing-card-invest-range">
                For balances
                <span className="pricing-card-num-inline">
                  ${humanize(minInvest)}{maxInvest ? ` - $${humanize(maxInvest)}` : `+`}
                </span>
              </div>
              <div>
                <span className="pricing-card-label">Advice Fee</span>
                <span className="pricing-card-num-inline">${feePlan.adviceFee}</span>
              </div>
              <div>
                <span className="pricing-card-label">Management Fee</span>
                <span className="pricing-card-num-inline">
                  {this.getManagementFeeDisplay(feePlan)}
                </span>
              </div>
              <div>
                <span className="pricing-card-label">Fees Saved</span>
                <span className="pricing-card-num-inline">{this.getAvgSavings(feePlan)}*</span>
              </div>
              <FeeMonthsFree monthsFree={feePlan.monthsFree} />
              <FeeThemesFree themesFree={feePlan.themesFree} />
              <FeeAverageSavingsFinePrint />
            </CardText>
          </div>
        </Card>
      </div>
    );
  }

  render() {
    return (
      <div className="row" id="fee-plans">
        {_map.default(FEES, this.renderPlan.bind(this))}
      </div>
    );
  }
}

