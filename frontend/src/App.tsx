import { Dashboard } from '@mui/icons-material';
import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import './App.css';
import MOOCletView from './Components/MOOCletView/MOOCletView';
import Preferences from './Components/Preferences/Preferences';

function App(): JSX.Element {
  return (
    <div className="app-wrapper">
      <h1>Application</h1>
      <BrowserRouter>
        <Switch>
          {/* ADD ROUTES HERE */}
          <Route exact path="/" render={() => <h1>Hello World</h1>} />
          <Route exact path="/dashboard">
            <Dashboard />
          </Route>
          <Route exact path="/preferences">
            <Preferences />
          </Route>
          <Route exact path="/mooclet" render={() => <MOOCletView moocletId={null} />} />
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
