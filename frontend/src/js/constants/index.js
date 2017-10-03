export const MANAGEMENT_FEE_TYPE_FLAT = 'managemet_fee_type_flat';
export const MANAGEMENT_FEE_TYPE_PCT = 'managemet_fee_type_pct';

export const MIN_INVEST_AMOUNT = 2000;
export const FEES_ROUNDING_PLACES = 2;

export const FEES = {
  'Bronze': {
    adviceFee: 0,
    managementFeeMonthly: 6.60,
    managementFeeType: MANAGEMENT_FEE_TYPE_FLAT,
    minInvestAmount: MIN_INVEST_AMOUNT,
    maxInvestAmount: 10000,
    monthsFree: 6,
    themesFree: false,
    avgSavingsRatio: 1.05,  // arbitrary
    color: '#FFD9B1',  // I don't like this being here...
  },
  'Silver': {
    adviceFee: 0,
    managementFeeMonthly: 0.00066,
    managementFeeType: MANAGEMENT_FEE_TYPE_PCT,
    minInvestAmount: 10001,
    maxInvestAmount: 49999,
    monthsFree: 0,
    themesFree: false,
    avgSavingsRatio: 1.10,  // arbitrary
    color: '#EFEFEF',  // I don't like this being here...
  },
  'Gold': {
    adviceFee: 55,
    managementFeeMonthly: 0.00055,
    managementFeeType: MANAGEMENT_FEE_TYPE_PCT,
    minInvestAmount: 50000,
    maxInvestAmount: 499999,
    monthsFree: 0,
    themesFree: true,
    avgSavingsRatio: 1.15,  // arbitrary
    color: '#F5DEB3',  // I don't like this being here...
  },
  'Platnium': {
    adviceFee: 55,
    managementFeeMonthly: 0.00044,
    managementFeeType: MANAGEMENT_FEE_TYPE_PCT,
    minInvestAmount: 500000,
    maxInvestAmount: undefined,
    monthsFree: 0,
    themesFree: true,
    avgSavingsRatio: 1.2,  // arbitrary
    color: '#CCCCCC',  // I don't like this being here...
  },
};
