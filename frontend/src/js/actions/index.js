import * as _find from 'lodash/find';

import { UPDATE_MONTHLY_FEE, AMOUNT_INPUT_CHANGED } from './types';
import { FEES, MANAGEMENT_FEE_TYPE_PCT, FEES_ROUNDING_PLACES } from '../constants';
import { round } from '../utils/number';

/**
 * We need to know when the input has changed so we can update UI
 */
export const amountInputChanged = () => {
  return {
    type: AMOUNT_INPUT_CHANGED
  };
};

/**
 * Calculate monthly fees.
 * Return a number (rounded where appropriate) or null as payload.
 */
export const updateAmountInput = (amountInput) => {
  // round amount so I can exactly match existing Stockspot pricing strucutre
  amountInput = Math.round(amountInput);

  let monthlyFee = null;

  const feePlan = _find.default(FEES, (feePlan) => {
    return amountInput >= feePlan.minInvestAmount && (
      amountInput <= feePlan.maxInvestAmount || !feePlan.maxInvestAmount);
  }) || null;

  if (feePlan) {
    monthlyFee = feePlan.managementFeeMonthly;
    if (feePlan.managementFeeType === MANAGEMENT_FEE_TYPE_PCT){
      monthlyFee += feePlan.adviceFee + (feePlan.managementFeeMonthly * amountInput);
    }
  }

  if (monthlyFee) {
    monthlyFee = round(monthlyFee, FEES_ROUNDING_PLACES);
  }

  return {
    type: UPDATE_MONTHLY_FEE,
    payload: {
      monthlyFee: monthlyFee,
      feePlan: feePlan
    }
  };
};
