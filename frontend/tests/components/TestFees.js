import React , { Component } from 'react';
import chai, { expect } from 'chai';
import { describe, it, beforeEach } from 'mocha';
import ReactTestUtils from 'react-dom/test-utils';

import { renderComponent } from '../helpers';
import Fees from '../../src/js/components/Fees';

describe('FeePlans', () => {
  let component;

  beforeEach(() => {
    component = renderComponent(Fees);
  });

  it("Has an amount input", () => {
    const amountInput = ReactTestUtils.findRenderedDOMComponentWithTag(component, 'input');
    expect(amountInput).to.exist;
  });

  it("Changing amount input changes the input's value", () => {
    const amountInput = ReactTestUtils.findRenderedDOMComponentWithTag(component, 'input');
    const val = '100';
    ReactTestUtils.Simulate.change(amountInput, {target: { value: val }});
    expect(amountInput.value).to.equal(val);
  });
});
