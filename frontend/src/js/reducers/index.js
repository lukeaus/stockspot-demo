import { combineReducers } from 'redux';
import monthlyFee from './monthlyFee';
import feePlan from './feePlan';
import feeCalcComplete from './feeCalcComplete';

const rootReducer = combineReducers({
  monthlyFee,
  feePlan,
  feeCalcComplete
});

export default rootReducer;
