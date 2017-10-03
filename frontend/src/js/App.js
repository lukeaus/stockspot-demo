import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import Fees from './components/fees';

export default class App extends Component {
  render() {
    return (
      <MuiThemeProvider>
        <Fees />
      </MuiThemeProvider>
    );
  }
}
