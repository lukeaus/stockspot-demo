import { UPDATE_MONTHLY_FEE } from '../actions/types';

export default (state = null, action) => {
  switch(action.type) {
  case UPDATE_MONTHLY_FEE:
    return action.payload.monthlyFee;
  default:
    return state;
  }
};

