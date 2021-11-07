import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import './App.css';
import MOOCletView from './Components/MOOCletView/MOOCletView';
import Login from './Components/Login/Login';
import Preferences from './Components/Preferences/Preferences';
import useToken from './Components/useToken';
import Dashboard from './Components/Dashboard/Dashboard';
import MOOCletDashboard from './Components/Dashboard/MOOCletDashboard';

function App(): JSX.Element {
  const { token, setToken } = useToken();
  //alert(token);
  if (!token) {
    return <Login setToken={setToken} />;
  }

  return (
    <div className="app-wrapper">
      {/* <h1>Application</h1> */}
      <BrowserRouter>
        <Switch>
          {/* ADD ROUTES HERE */}
          <Route exact path="/" render={() => <h1>Hello World</h1>} />
          <Route exact path="/dashboard" render={() => <Dashboard />}>
            <Dashboard />
          </Route>
          <Route exact path="/moocletdashboard" render={() => <MOOCletDashboard />}>
            <MOOCletDashboard />
          </Route>
          <Route exact path="/preferences">
            <Preferences />
          </Route>
          <Route exact path="/mooclet" render={() => <MOOCletView userId={0} organizationId={0} />} />
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
