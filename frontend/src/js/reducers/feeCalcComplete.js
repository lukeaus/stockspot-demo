import { UPDATE_MONTHLY_FEE, AMOUNT_INPUT_CHANGED } from '../actions/types';

export default (state = null, action) => {
  switch(action.type) {
  case AMOUNT_INPUT_CHANGED:
    return false;
  case UPDATE_MONTHLY_FEE:
    // note that there may not be an applicable monthly fee or fee plan, but calculations complete
    return true;
  default:
    return state;
  }
};
