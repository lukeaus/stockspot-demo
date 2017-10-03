import * as _round from 'lodash/round';
import numeral from 'numeral';

/**
 * Ensure that rounded numbers *always* has the correct number of places
 */
export const round = (number, places = 2) => {
  return _round.default(number, places).toFixed(places);
};

/**
 * Take a number and make it human readable
 * e.g. 499999 => 499,999
 */
export const humanize = (number) => {
  const hasDecimalPlaces = number.toString().split('.').length > 1;
  if (hasDecimalPlaces) {
    const decimalVal = number.toString().split('.')[1];
    const decimalPlacesValIsZero = !/[^0*]/.test(decimalVal);
    if (decimalPlacesValIsZero) {
      return humanizeThousandsSep(number);
    }
    return humanizeThousandsSepDecimals(number);
  } else {
    return humanizeThousandsSep(number);
  }
};

const humanizeThousandsSep = (number) => numeral(number).format('0,0');
const humanizeThousandsSepDecimals = (number) => numeral(number).format('0,0.00');
