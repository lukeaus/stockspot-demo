import chai, { expect } from 'chai';
import { describe, it } from 'mocha';

import feeCalcComplete from '../../src/js/reducers/FeeCalcComplete';
import { UPDATE_MONTHLY_FEE, AMOUNT_INPUT_CHANGED } from '../../src/js/actions/types';

describe('FeeCalcComplete Reducer', () => {
  it('handles action with unknown type', () => {
    expect(feeCalcComplete(null, {})).to.eql(null);
  });

  it('handles action with type UPDATE_MONTHLY_FEE', () => {
    const action = { type: UPDATE_MONTHLY_FEE };
    expect(feeCalcComplete(null, action)).to.eql(true);
  });

  it('handles action with type AMOUNT_INPUT_CHANGED', () => {
    const action = { type: AMOUNT_INPUT_CHANGED };
    expect(feeCalcComplete(null, action)).to.eql(false);
  });
});
