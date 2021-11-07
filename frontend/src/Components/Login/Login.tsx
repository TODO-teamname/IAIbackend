import React, { useState } from 'react';
import PropTypes from 'prop-types';
import '../../styles/Login.css';
import { useHistory } from 'react-router-dom';

async function loginUser(credentials) {
  return fetch('http://localhost:8080/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  }).then((data) => data.json());
}

export default function Login({ setToken }) {
  const [username, setUserName] = useState<string | null>('');
  const [password, setPassword] = useState<string | null>('');

  //const history = useHistory();
  //const handleLogin = () => {
  //  history.push('/dashboard');
  //};
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username?.localeCompare('Test') && !password?.localeCompare('123')) {
      const token = [username, password];
      //const token = await loginUser({
      //  username,
      //  password,
      //});
      setToken(token);
      window.location.href = './dashboard';
      //handleLogin();
    }
  };

  return (
    <div className="login-wrapper">
      <h1 className="main-header">Please Log In</h1>
      <form onSubmit={handleSubmit}>
        <label>
          <p>Username</p>
          <input type="text" onChange={(e) => setUserName(e.target.value)} />
        </label>
        <label>
          <p>Password</p>
          <input type="password" onChange={(e) => setPassword(e.target.value)} />
        </label>
        <div>
          <input type="submit" value="Log in" />
        </div>
      </form>
    </div>
  );
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired,
};
