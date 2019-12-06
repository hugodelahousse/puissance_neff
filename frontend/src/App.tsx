import React from 'react';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import { BrowserRouter as Router } from 'react-router-dom';
import Routes from './Routes';
import Layout from './views/layout/Layout';

import Connect4Board from './views/connect4board/Connect4Board';

const theme = createMuiTheme({
  palette: {
    type: 'dark',
  },
});

const App: React.FC = () => {
  return (
    <Router>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Layout>
          <Routes />
          <Connect4Board gameId="test1" />
        </Layout>
      </ThemeProvider>
    </Router>
  );
};

export default App;
