import { UPDATE_MONTHLY_FEE } from '../actions/types';

export default (state = null, action) => {
  switch(action.type) {
  case UPDATE_MONTHLY_FEE:
    return action.payload.feePlan;
  default:
    return state;
  }
};

