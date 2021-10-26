import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import './App.css';
import MOOCletView from './Components/MOOCletView/MOOCletView';

function App(): JSX.Element {
  return (
    <BrowserRouter>
      <Switch>
        {/* ADD ROUTES HERE */}
        <Route exact path="/" render={() => <h1>Hello World</h1>} />
        <Route exact path="/mooclet" render={() => <MOOCletView />} />
      </Switch>
    </BrowserRouter>
  );
}

export default App;
