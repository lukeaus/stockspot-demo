import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';

import App from './App';
import reducers from './reducers';

// should work...doesn't work...More investigation needed. Error: "Webpack: Failed to compile."
// Ref: https://raw.githubusercontent.com/twbs/bootstrap/v4-dev/docs/4.0/getting-started/webpack.md
// import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import '../style/styles.css';


const createStoreWithMiddleware = applyMiddleware()(createStore);

ReactDOM.render(
  <Provider store={createStoreWithMiddleware(reducers)}>
    <App />
  </Provider>,
  document.querySelector('.container'));
