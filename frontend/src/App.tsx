import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import './App.css';

function App(): JSX.Element {
  return (
    <BrowserRouter>
      <Switch>
        {/* ADD ROUTES HERE */}
        <Route path="/" render={() => <h1>Hello World</h1>} />
      </Switch>
    </BrowserRouter>
  );
}

export default App;
