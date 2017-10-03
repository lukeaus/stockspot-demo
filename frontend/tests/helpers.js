import React from 'react';
import 'jsdom-global/register';  // no config required
import ReactTestUtils from 'react-dom/test-utils';
import ReactDOM from 'react-dom';
import { createStore } from 'redux';
import { Provider } from 'react-redux';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import rootReducer from '../src/js/reducers';

// need to build 'renderComponent' helper that should render a given react class
// TODO: this feels like a lot of duplication with App...look into this
function renderComponent(ComponentClass, props, state) {
  const componentInstance = ReactTestUtils.renderIntoDocument(
    <Provider store={createStore(rootReducer, state)}>
      <MuiThemeProvider>
        <ComponentClass {...props} />
      </MuiThemeProvider>
    </Provider>
  );

  return componentInstance;
}

export { renderComponent };
